#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <time.h>
#include <poll.h>

#define MAX_LINE 256

typedef struct {
    int row;
    int col;
} task;

typedef struct {
    int **A;
    int **B;
    int **C;
    int size;
    task *task_queue;
    int *task_index;
    int task_count;
    pthread_mutex_t *task_mutex;
} threaddata;

void *thread_function(void *arg) {
    threaddata *data = (threaddata *)arg;

    //printf("[THREAD %ld] Started\n", pthread_self()); fflush(stdout);

    while (1) {
        pthread_mutex_lock(data->task_mutex);

        int idx = *(data->task_index);
        if (idx >= data->task_count) {
            pthread_mutex_unlock(data->task_mutex);
            //printf("[THREAD %ld] No more tasks, exiting\n", pthread_self()); fflush(stdout);
            break;
        }

        (*data->task_index)++;
        pthread_mutex_unlock(data->task_mutex);

        task t = data->task_queue[idx];

        //printf("[THREAD %ld] Computing task: C[%d][%d]\n", pthread_self(), t.row, t.col); fflush(stdout);

        int sum = 0;
        for (int k = 0; k < data->size; k++) {
            sum += data->A[t.row][k] * data->B[k][t.col];
        }

        data->C[t.row][t.col] = sum;

        //printf("[THREAD %ld] Finished task: C[%d][%d] = %d\n", pthread_self(), t.row, t.col, sum); fflush(stdout);
    }

    //printf("[THREAD %ld] Exiting normally\n", pthread_self()); fflush(stdout);
    free(data);
    return NULL;
}

int **allocate_matrix(int size) {
    int **matrix = malloc(size * sizeof(int*));
    for (int i = 0; i < size; i++)
        matrix[i] = malloc(size * sizeof(int));
    return matrix;
}

void free_matrix(int **matrix, int size) {
    for (int i = 0; i < size; i++)
        free(matrix[i]);
    free(matrix);
}

void generate_matrix(int **matrix, int size) {
    for (int i = 0; i < size; ++i)
        for (int j = 0; j < size; ++j)
            matrix[i][j] = rand() % 10;
}

void save_matrix(int **matrix, int size, const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("[MAIN] Failed to open output file");
        return;
    }

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++)
            fprintf(f, "%d ", matrix[i][j]);
        fprintf(f, "\n");
    }
    fclose(f);
}

ssize_t read_all(int fd, void *buf, size_t count) {
    size_t total = 0;
    while (total < count) {
        ssize_t r = read(fd, (char*)buf + total, count - total);
        if (r <= 0) return r;
        total += r;
    }
    return total;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <num_processes> <num_threads>\n", argv[0]);
        return 1;
    }

    int num_processes = atoi(argv[1]);
    int num_threads = atoi(argv[2]);

    srand(time(NULL));
    const char *fifo_name = "zadania.in";
    mkfifo(fifo_name, 0666);
    printf("[MAIN] Waiting for tasks in %s...\n", fifo_name);

    int fds_in[num_processes][2], fds_out[num_processes][2];
    pid_t children[num_processes];

    for (int i = 0; i < num_processes; i++) {
        pipe(fds_in[i]);
        pipe(fds_out[i]);

        pid_t pid = fork();
        if (pid == 0) {
            close(fds_in[i][1]);
            close(fds_out[i][0]);

            int child_index;
            read(fds_in[i][0], &child_index, sizeof(int));

            while (1) {
                int size;
                if (read(fds_in[i][0], &size, sizeof(int)) <= 0 || size == -1)
                    break;

                int **A = allocate_matrix(size);
                int **B = allocate_matrix(size);
                int **C = allocate_matrix(size);

                for (int r = 0; r < size; r++)
                    read_all(fds_in[i][0], A[r], sizeof(int) * size);
                for (int r = 0; r < size; r++)
                    read_all(fds_in[i][0], B[r], sizeof(int) * size);

                int total = size * size;
                int base = total / num_processes;
                int extra = total % num_processes;
                int start = base * child_index + (child_index < extra ? child_index : extra);
                int end = start + base + (child_index < extra ? 1 : 0);

                int my_task_count = end - start;
                task *tasks = malloc(sizeof(task) * my_task_count);
                for (int idx = 0; idx < my_task_count; idx++) {
                    int t = start + idx;
                    tasks[idx].row = t / size;
                    tasks[idx].col = t % size;
                }

                pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
                pthread_t threads[num_threads];
                int *shared_index = malloc(sizeof(int));
                *shared_index = 0;
                pthread_mutex_t *shared_mutex = malloc(sizeof(pthread_mutex_t));
                pthread_mutex_init(shared_mutex, NULL);

                for (int t = 0; t < num_threads; t++) {
                    threaddata *data = malloc(sizeof(threaddata));
                    data->A = A;
                    data->B = B;
                    data->C = C;
                    data->size = size;
                    data->task_queue = tasks;
                    data->task_index = shared_index;
                    data->task_count = my_task_count;
                    data->task_mutex = shared_mutex;

                    pthread_create(&threads[t], NULL, thread_function, data);
                }

                for (int t = 0; t < num_threads; t++)
                    pthread_join(threads[t], NULL);

                pthread_mutex_destroy(&mutex);
                free(shared_mutex);
                free(shared_index);

                for (int j = 0; j < my_task_count; j++) {
                    int r = tasks[j].row;
                    int c = tasks[j].col;
                    int value = C[r][c];

                    //printf("[CHILD %d] Sending result C[%d][%d] = %d\n", child_index, r, c, value);
                    //fflush(stdout);

                    write(fds_out[i][1], &r, sizeof(int));
                    write(fds_out[i][1], &c, sizeof(int));
                    write(fds_out[i][1], &value, sizeof(int));
                }

                free_matrix(A, size);
                free_matrix(B, size);
                free_matrix(C, size);
                free(tasks);
            }

            exit(0);
        }

        children[i] = pid;
        close(fds_in[i][0]);
        close(fds_out[i][1]);

        write(fds_in[i][1], &i, sizeof(int));
    }

    int fifo_fd = open(fifo_name, O_RDONLY);
    int dummy_fd = open(fifo_name, O_WRONLY);

    FILE *fifo = fopen(fifo_name, "r");
    char line[MAX_LINE];
    while (fgets(line, sizeof(line), fifo)) {
        if (strncmp(line, "EXIT", 4) == 0) {
            printf("[MAIN] Shutting down...\n");
            for (int i = 0; i < num_processes; i++) {
                int term = -1;
                write(fds_in[i][1], &term, sizeof(int));
                close(fds_in[i][1]);
                close(fds_out[i][0]);
            }
            for (int i = 0; i < num_processes; i++)
                waitpid(children[i], NULL, 0);
            break;
        }

        int size;
        char filename[128];
        if (sscanf(line, "%d %s", &size, filename) != 2) continue;

        printf("[MAIN] Received task: %dx%d matrix -> %s\n", size, size, filename);

        int **A = allocate_matrix(size);
        int **B = allocate_matrix(size);
        int **C = allocate_matrix(size);
        generate_matrix(A, size);
        generate_matrix(B, size);

        for (int i = 0; i < num_processes; i++) {
            write(fds_in[i][1], &size, sizeof(int));
            for (int r = 0; r < size; r++)
                write(fds_in[i][1], A[r], sizeof(int) * size);
            for (int r = 0; r < size; r++)
                write(fds_in[i][1], B[r], sizeof(int) * size);
        }

        struct pollfd pfds[num_processes];
        for (int i = 0; i < num_processes; i++) {
            pfds[i].fd = fds_out[i][0];
            pfds[i].events = POLLIN;
        }

        int total = size * size;
        int received = 0;
        while (received < total) {
            int ready = poll(pfds, num_processes, -1);
            if (ready < 0) {
                perror("poll");
                break;
            }
        
            for (int i = 0; i < num_processes; i++) {
                if (pfds[i].revents & POLLIN) {
                    int r, c, val;
                    if (read_all(fds_out[i][0], &r, sizeof(int)) == sizeof(int) &&
                        read_all(fds_out[i][0], &c, sizeof(int)) == sizeof(int) &&
                        read_all(fds_out[i][0], &val, sizeof(int)) == sizeof(int)) {
                        C[r][c] = val;
                        received++;
                    }
                }
            }
        }

        save_matrix(C, size, filename);
        free_matrix(A, size);
        free_matrix(B, size);
        free_matrix(C, size);
        printf("[MAIN] Task saved to %s\n", filename);
    }

    close(fifo_fd);
    close(dummy_fd);
    fclose(fifo);
    unlink(fifo_name);

    return 0;
}
