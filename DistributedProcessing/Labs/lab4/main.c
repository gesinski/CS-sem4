#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>
#include <time.h>
#include <stdlib.h>

long long compute(int n) {
    long long fib0 = 1, fib1 = 1;
    if (n == 1 || n == 2) return 1;
    
    n -= 2;
    while (n--) {
        long long tmp = fib1;
        fib1 += fib0;
        fib0 = tmp;
    }
    return fib1;
}

long long compute_count(long long n) {
    return n-2;
}

void *thread_function(void *arg) {
    int thread_num = *(int *)arg;
    free(arg);
    
    clock_t start = clock();
    
    compute(1000000000);
    
    clock_t end = clock();
    double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Thread %d finished in %f seconds\n", thread_num, elapsed_time);
    return NULL;
}

int main(int argc, char *argv[]) {
    clock_t start, end;
    double elapsed_time;

    start = clock(); 
    if (argc != 3) {
        printf("Usage: %s <number_of_processes> <number_of_threads>\n", argv[0]);
        return 1;
    }

    int num_processes = atoi(argv[1]);
    int num_threads = atoi(argv[2]);

    printf("Creating %d processes, each with %d threads.\n", num_processes, num_threads);

    for (int i = 0; i < num_processes; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            pthread_t threads[num_threads];
            for (int j = 0; j < num_threads; j++) {
                int* thread_id = malloc(sizeof(int));
                *thread_id = i * num_threads + j;
                if (pthread_create(&threads[j], NULL, thread_function, thread_id) != 0) {
                    perror("Failed to create thread");
                    exit(1);
                }

            }

            for (int j = 0; j < num_threads; j++) {
                pthread_join(threads[j], NULL);
            }

            end = clock();  
            double elapsed_time = (double)(end - start) / CLOCKS_PER_SEC;
            printf("Operations per second: %e\n", (compute_count(1000000000)*num_threads*num_processes / elapsed_time));

            printf("Process %d finished in %f seconds\n", i, elapsed_time);
            
            exit(0);
        }
    }

    for (int i = 0; i < num_processes; i++) {
        wait(NULL);
    }

    return 0;
}
