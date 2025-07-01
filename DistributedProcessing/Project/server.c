#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <math.h>

#define MAX_CLIENTS 2
#define MAP_WIDTH 800
#define MAP_HEIGHT 400
#define PLAYER_RADIUS 15
#define PUCK_RADIUS 15
#define FRICTION 0.85f
#define PUCK_HIT_SPEED_MULTIPLIER 2.0f

int player_count = 0;
// Starting positions of players
const int start_pos[MAX_CLIENTS][2] = { {100, 200}, {MAP_WIDTH - 100, 200} };

int player_pos[MAX_CLIENTS][2];
int puck_x = MAP_WIDTH / 2, puck_y = MAP_HEIGHT / 2;
float puck_vx = 0.0f, puck_vy = 0.0f;
int score[2] = {0, 0};
int goal_height = 100;

pthread_mutex_t lock;

float distance(int x1, int y1, int x2, int y2) {
    return sqrtf((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1));
}

void reset_positions() {
    for (int i = 0; i < MAX_CLIENTS; i++) {
        player_pos[i][0] = start_pos[i][0];
        player_pos[i][1] = start_pos[i][1];
    }
    puck_x = MAP_WIDTH / 2;
    puck_y = MAP_HEIGHT / 2;
    puck_vx = 0;
    puck_vy = 0;
}

void reset_player_position(int player) {
    player_pos[player][0] = start_pos[player][0];
    player_pos[player][1] = start_pos[player][1];
}

void update_puck() {
    // Update puck position
    puck_x += (int)puck_vx;
    puck_y += (int)puck_vy;

    // Apply friction
    puck_vx *= FRICTION;
    puck_vy *= FRICTION;

    // Bounce off walls
    int goal_top = (MAP_HEIGHT - goal_height) / 2;
    int goal_bottom = goal_top + goal_height;

    // LEFT GOAL
    if (puck_x <= PUCK_RADIUS) {
        if (puck_y > goal_top && puck_y < goal_bottom) {
            // Point for player 2
            score[1]++;

            // Reset positions of both players (not only player 2)
            reset_positions();

            // Reset puck position and velocity
            puck_x = MAP_WIDTH / 2;
            puck_y = MAP_HEIGHT / 2;
            puck_vx = 0;
            puck_vy = 0;

            return;
        } else {
            puck_x = PUCK_RADIUS;
            puck_vx = -puck_vx;
        }
    }

    // RIGHT GOAL
    if (puck_x >= MAP_WIDTH - PUCK_RADIUS) {
        if (puck_y > goal_top && puck_y < goal_bottom) {
            // Point for player 1
            score[0]++;

            // Reset positions of both players (not only player 1)
            reset_positions();

            // Reset puck position and velocity
            puck_x = MAP_WIDTH / 2;
            puck_y = MAP_HEIGHT / 2;
            puck_vx = 0;
            puck_vy = 0;

            return;
        } else {
            puck_x = MAP_WIDTH - PUCK_RADIUS;
            puck_vx = -puck_vx;
        }
    }


    if (puck_y <= PUCK_RADIUS) {
        puck_y = PUCK_RADIUS;
        puck_vy = -puck_vy;
    }
    if (puck_y >= MAP_HEIGHT - PUCK_RADIUS) {
        puck_y = MAP_HEIGHT - PUCK_RADIUS;
        puck_vy = -puck_vy;
    }
}

void *connection_handler(void *socket_desc) {
    int sock = *(int *)socket_desc;
    free(socket_desc);

    int read_size;
    char client_message[2000];
    char buffer[256];
    int assigned_player = -1;

    pthread_mutex_lock(&lock);
    if (player_count < MAX_CLIENTS) {
        assigned_player = player_count;
        player_count++;

        // Set players' starting positions
        player_pos[assigned_player][0] = start_pos[assigned_player][0];
        player_pos[assigned_player][1] = start_pos[assigned_player][1];

        fprintf(stderr, "Assigned player %d\n", assigned_player + 1);
        fflush(stderr);
    }
    pthread_mutex_unlock(&lock);

    if (assigned_player == -1) {
        write(sock, "Server full\n", 12);
        close(sock);
        pthread_exit(NULL);
    }

    fprintf(stderr, "Player %d connected\n", assigned_player + 1);

    snprintf(buffer, sizeof(buffer), "player_id:%d\n", assigned_player);
    write(sock, buffer, strlen(buffer));

    while ((read_size = recv(sock, client_message, sizeof(client_message) - 1, 0)) > 0) {
        client_message[read_size] = '\0';

        if (strncmp(client_message, "status", 6) == 0) {
            pthread_mutex_lock(&lock);
            snprintf(buffer, sizeof(buffer), "players:%d\n", player_count);
            pthread_mutex_unlock(&lock);
            write(sock, buffer, strlen(buffer));
        } 
        else if (strncmp(client_message, "ping", 4) == 0) {
            int x, y;
            if (sscanf(client_message, "ping %d %d", &x, &y) == 2) {
                if (x > 0 && y > 0) {
                    pthread_mutex_lock(&lock);

                    int prev_x = player_pos[assigned_player][0];
                    int prev_y = player_pos[assigned_player][1];

                    // Update player position
                    player_pos[assigned_player][0] = x;
                    player_pos[assigned_player][1] = y;

                    // Prevent players from overlapping
                    int other = 1 - assigned_player;
                    float dist_players = distance(player_pos[assigned_player][0], player_pos[assigned_player][1], player_pos[other][0], player_pos[other][1]);
                    if (dist_players < 2 * PLAYER_RADIUS) {
                        // Revert move
                        player_pos[assigned_player][0] = prev_x;
                        player_pos[assigned_player][1] = prev_y;
                    }

                    // Collision with puck
                    float dist = distance(player_pos[assigned_player][0], player_pos[assigned_player][1], puck_x, puck_y);
                    if (dist < PLAYER_RADIUS + PUCK_RADIUS) {
                        // Give puck velocity based on player movement * speed multiplier
                        float dx = x - prev_x;
                        float dy = y - prev_y;

                        puck_vx = dx * PUCK_HIT_SPEED_MULTIPLIER;
                        puck_vy = dy * PUCK_HIT_SPEED_MULTIPLIER;
                    }

                    // Update puck position and wall bounces
                    update_puck();

                    pthread_mutex_unlock(&lock);
                }
            }

            pthread_mutex_lock(&lock);
            snprintf(buffer, sizeof(buffer), "%d %d %d %d %d %d %d %d\n",
                player_pos[0][0], player_pos[0][1],
                player_pos[1][0], player_pos[1][1],
                puck_x, puck_y,
                score[0], score[1]);
            pthread_mutex_unlock(&lock);

            write(sock, buffer, strlen(buffer));
        }

        memset(client_message, 0, sizeof(client_message));
    }

    fprintf(stderr, "Player %d disconnected\n", assigned_player + 1);

    pthread_mutex_lock(&lock);
    player_count--;
    pthread_mutex_unlock(&lock);

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    int listenfd = 0, connfd = 0;
    struct sockaddr_in serv_addr;
    pthread_t thread_id;

    pthread_mutex_init(&lock, NULL);

    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(2137);

    bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    listen(listenfd, 10);

    fprintf(stderr, "Server listening on port 2137...\n");

    reset_positions();

    while (1) {
        connfd = accept(listenfd, NULL, NULL);
        int *new_sock = malloc(sizeof(int));
        *new_sock = connfd;

        pthread_create(&thread_id, NULL, connection_handler, (void *)new_sock);
        pthread_detach(thread_id);
    }

    pthread_mutex_destroy(&lock);
    return 0;
}
