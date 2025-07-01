#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <time.h>
#include <sys/mman.h>
#include <string.h>

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

    while (1) {
        pthread_mutex_lock(data->task_mutex);
        if (*(data->task_index) >= data->task_count) {
            pthread_mutex_unlock(data->task_mutex);
            break;
        }

        task t = data->task_queue[(*(data->task_index))++];
        pthread_mutex_unlock(data->task_mutex);

        int sum = 0;
        for (int k = 0; k < data->size; k++) {
            sum += data->A[t.row][k] * data->B[k][t.col];
        }
        data->C[t.row][t.col] = sum;
    }

    free(data);
    return NULL;
}

void generate_matrix(int **matrix, int size) {
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            matrix[i][j] = rand() % 100;
        }
    }
}

int main(int argc, char *argv[]) {
    srand(time(NULL));

    if (argc != 4) {
        printf("Usage: %s <matrix_size> <num_processes> <num_threads>\n", argv[0]);
        return 1;
    }

    int matrix_size = atoi(argv[1]);
    int num_processes = atoi(argv[2]);
    int num_threads = atoi(argv[3]);

    int **matrix1 = malloc(matrix_size * sizeof(int*));
    int **matrix2 = malloc(matrix_size * sizeof(int*));
    for (int i = 0; i < matrix_size; i++) {
        matrix1[i] = malloc(matrix_size * sizeof(int));
        matrix2[i] = malloc(matrix_size * sizeof(int));
    }
    generate_matrix(matrix1, matrix_size);
    generate_matrix(matrix2, matrix_size);

    int **matrix_final = mmap(NULL, sizeof(int*) * matrix_size, PROT_READ | PROT_WRITE,
                              MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    for (int i = 0; i < matrix_size; i++) {
        matrix_final[i] = mmap(NULL, sizeof(int) * matrix_size, PROT_READ | PROT_WRITE,
                               MAP_SHARED | MAP_ANONYMOUS, -1, 0);
        memset(matrix_final[i], 0, sizeof(int) * matrix_size);
    }

    int task_count = matrix_size * matrix_size;
    task *task_queue = mmap(NULL, sizeof(task) * task_count, PROT_READ | PROT_WRITE,
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int index = 0;
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            task_queue[index++] = (task){i, j};
        }
    }

    int *shared_index = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE,
                             MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    *shared_index = 0;

    pthread_mutex_t *mutex = mmap(NULL, sizeof(pthread_mutex_t), PROT_READ | PROT_WRITE,
                                  MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    pthread_mutexattr_t attr;
    pthread_mutexattr_init(&attr);
    pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED);
    pthread_mutex_init(mutex, &attr);

    printf("Creating %d processes, each with %d threads to calculate matrix.\n", num_processes, num_threads);

    for (int i = 0; i < num_processes; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            pthread_t threads[num_threads];
            for (int j = 0; j < num_threads; j++) {
                threaddata *thread_data = malloc(sizeof(threaddata));
                thread_data->A = matrix1;
                thread_data->B = matrix2;
                thread_data->C = matrix_final;
                thread_data->size = matrix_size;
                thread_data->task_queue = task_queue;
                thread_data->task_index = shared_index;
                thread_data->task_count = task_count;
                thread_data->task_mutex = mutex;

                if (pthread_create(&threads[j], NULL, thread_function, thread_data) != 0) {
                    perror("Failed to create thread");
                    exit(1);
                }
            }

            for (int j = 0; j < num_threads; j++) {
                pthread_join(threads[j], NULL);
            }

            exit(0);
        }
    }

    for (int i = 0; i < num_processes; i++) {
        wait(NULL);
    }

    
    int **matrixes[3] = {matrix1, matrix2, matrix_final};
        
    for(int i = 0; i < 3; i++) {
        printf("Matrix: %d\n", i);
        for (int row = 0; row < matrix_size; row++) {
            for (int col = 0; col < matrix_size; col++) {
                printf("%d ", matrixes[i][row][col]);
            }
            printf("\n");
        }
        printf("\n");
    }
    
    free(matrix1);
    free(matrix2);
    munmap(matrix_final, sizeof(int*) * matrix_size);
    munmap(task_queue, sizeof(task) * task_count);
    munmap(shared_index, sizeof(int));
    pthread_mutex_destroy(mutex);
    munmap(mutex, sizeof(pthread_mutex_t));

    return 0;
}
