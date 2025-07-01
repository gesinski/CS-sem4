import socket
import pygame
import sys
import time

# --- GAME CONSTANTS ---
WIDTH, HEIGHT = 800, 400
FPS = 60
PUCK_RADIUS = 15
PLAYER_RADIUS = 15
PLAYER_SPEED = 5
WAIT_AFTER_GOAL_SECONDS = 2  # wait time after scoring a goal (in seconds)

# --- SERVER CONNECTION INITIALIZATION ---
def connect_to_server(address="localhost", port=2137):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
        raw_id_msg = s.recv(1024).decode().strip()
        if raw_id_msg.startswith("player_id:"):
            player_id = int(raw_id_msg.split(":")[1])
            print(f"Received player_id: {player_id}")
            return s, player_id
        else:
            print("Did not receive player_id, closing.")
            s.close()
            sys.exit()
    except Exception as e:
        print(f"Error connecting to server: {e}")
        s.close()
        sys.exit()

# --- PYGAME AND SCREEN INITIALIZATION ---
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cymbergej")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    return screen, clock, font

# --- WAITING FOR PLAYERS MENU ---
def draw_waiting_screen(screen, font, player_count):
    screen.fill((200, 200, 200))
    title = font.render("Waiting for players...", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    p1_status = "Player 1: Connected" if player_count >= 1 else "Player 1: Waiting..."
    p2_status = "Player 2: Connected" if player_count >= 2 else "Player 2: Waiting..."

    p1_text = font.render(p1_status, True, (0, 0, 255))
    p2_text = font.render(p2_status, True, (0, 0, 255))

    screen.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, HEIGHT // 2))
    screen.blit(p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def wait_for_players(sock, screen, clock, font):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sock.close()
                sys.exit()

        try:
            sock.sendall(b"status\n")
            response = sock.recv(1024).decode().strip()
            if response.startswith("players:"):
                player_count = int(response.split(":")[1])
                draw_waiting_screen(screen, font, player_count)
                if player_count == 2:
                    return
        except Exception as e:
            print(f"Connection error while waiting: {e}")
            pygame.quit()
            sock.close()
            sys.exit()

        clock.tick(2)  # Update every 0.5 seconds

# --- FETCH INITIAL POSITIONS AND SCORE ---
def get_initial_state(sock, player_id):
    try:
        sock.sendall(b"ping -1 -1\n")
        data = sock.recv(1024).decode().strip()
        parts = data.split()
        if len(parts) == 8:
            if player_id == 0:
                player_pos = (int(parts[0]), int(parts[1]))
            else:
                player_pos = (int(parts[2]), int(parts[3]))
            score1 = int(parts[6])
            score2 = int(parts[7])
            return player_pos[0], player_pos[1], score1, score2
    except Exception as e:
        print(f"Error fetching initial position, setting default: {e}")
    return 100, HEIGHT // 2, 0, 0

# --- DRAWING ELEMENTS ON SCREEN ---
def draw_field(screen):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 6)
    pygame.draw.line(screen, (0, 0, 0), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)

    # Goal
    goal_depth = 30
    goal_height = 100
    goal_thickness = 6
    goal_y = (HEIGHT - goal_height) // 2

    # Left goal
    pygame.draw.line(screen, (255, 0, 0), (0, goal_y), (goal_depth, goal_y), goal_thickness)
    pygame.draw.line(screen, (255, 0, 0), (goal_depth, goal_y), (goal_depth, goal_y + goal_height), goal_thickness)
    pygame.draw.line(screen, (255, 0, 0), (0, goal_y + goal_height), (goal_depth, goal_y + goal_height), goal_thickness)

    # Right goal
    pygame.draw.line(screen, (255, 0, 0), (WIDTH, goal_y), (WIDTH - goal_depth, goal_y), goal_thickness)
    pygame.draw.line(screen, (255, 0, 0), (WIDTH - goal_depth, goal_y), (WIDTH - goal_depth, goal_y + goal_height), goal_thickness)
    pygame.draw.line(screen, (255, 0, 0), (WIDTH, goal_y + goal_height), (WIDTH - goal_depth, goal_y + goal_height), goal_thickness)

def draw_players_and_puck(screen, p1, p2, puck):
    pygame.draw.circle(screen, (0, 255, 0), p1, PLAYER_RADIUS)  # Player 1 - green
    pygame.draw.circle(screen, (255, 0, 0), p2, PLAYER_RADIUS)  # Player 2 - red
    pygame.draw.circle(screen, (0, 0, 255), puck, PUCK_RADIUS) # Puck - blue

def draw_score(screen, font, score1, score2):
    score_text = font.render(f"{score1} : {score2}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 100, 10))

def draw_info(screen, font, p1, p2, puck):
    info_text = font.render(f"P1: {p1}, P2: {p2}, Puck: {puck}", True, (0, 0, 0))
    screen.blit(info_text, (10, 10))

# --- MAIN GAME LOOP ---
def main():
    sock, player_id = connect_to_server()
    screen, clock, font = init_pygame()

    wait_for_players(sock, screen, clock, font)

    player_x, player_y, score1, score2 = get_initial_state(sock, player_id)
    prev_score1, prev_score2 = score1, score2

    waiting_after_goal = False
    wait_start_time = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            # Receive game state (before processing movement)
            msg = f"ping {player_x} {player_y}\n".encode()
            sock.sendall(msg)
            data = sock.recv(1024).decode().strip()
        except Exception:
            print("Lost connection to server")
            break

        parts = data.split()
        if len(parts) == 8:
            p1_pos = (int(parts[0]), int(parts[1]))
            p2_pos = (int(parts[2]), int(parts[3]))
            puck_pos = (int(parts[4]), int(parts[5]))
            score1 = int(parts[6])
            score2 = int(parts[7])

            # If goal scored, start waiting timer and reset local player position
            if (score1 != prev_score1 or score2 != prev_score2) and not waiting_after_goal:
                waiting_after_goal = True
                wait_start_time = time.time()
                # Update local player pos from server reset pos
                if player_id == 0:
                    player_x, player_y = p1_pos
                else:
                    player_x, player_y = p2_pos

            prev_score1, prev_score2 = score1, score2

        # Player movement only if not waiting after goal
        if not waiting_after_goal:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x += PLAYER_SPEED

            # Keep movement within field boundaries
            player_x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_x))
            player_y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_y))
        else:
            # Check if waiting time has passed
            if time.time() - wait_start_time >= WAIT_AFTER_GOAL_SECONDS:
                waiting_after_goal = False

        draw_field(screen)
        if len(parts) == 8:
            draw_players_and_puck(screen, p1_pos, p2_pos, puck_pos)
            draw_score(screen, font, score1, score2)
            draw_info(screen, font, p1_pos, p2_pos, puck_pos)

            if score1 >= 7 or score2 >= 7:
                winner = "Player 1" if score1 > score2 else "Player 2"
                screen.fill((0, 0, 0))
                win_text = font.render(f"{winner} wins!", True, (255, 255, 0))
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(3000)  # Pause 3 seconds to show result
                running = False

        pygame.display.flip()

    pygame.quit()
    sock.close()

if __name__ == "__main__":
    main()
