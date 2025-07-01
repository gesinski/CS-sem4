#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>
#include "linked_list.h"

int main() {
    struct element * list = innit_linked_list();
    clock_t start, end;
    double elapsed_time;

    start = time(NULL);
    
    printf("Procces %d is running\n", getpid());

    list->next = insert(100, list);
    printList(list);
    
    int pid = fork();

    if (pid == -1) {
        printf("fork failed");
        return 1;
    }
    else if (pid == 0) {
        printf("Child process (PID: %d) of Parent process (PID: %d) is running\n", getpid(), getppid());

        list->next = insert(101, list);
        printList(list);
        
        if (fork () == 0) {
            printf("Child process (PID: %d) of Parent process (PID: %d) is running\n", getpid(), getppid());

            delete(list, 1);
            printList(list);

            sleep(10);
            printf("Child process (PID: %d) is terminating.\n", getpid());
            free_linked_list(list);
            return 0;
        }
        sleep(5);
        wait(NULL);
        printList(list);
        printf("Child process (PID: %d) is terminating.\n", getpid());
        free_linked_list(list);
        return 0;
    }
    else {
        list->next = insert(102, list);
        if (fork () == 0) {
            printf("Child process (PID: %d) of Parent process (PID: %d) is running\n", getpid(), getppid());

            list->next = insert(103, list);
            printList(list);

            printf("Child process (PID: %d) is terminating.\n", getpid());
            free_linked_list(list);
            return 0;
        }
        int status;
        while (wait(&status) > 0);
        printList(list);
        printf("Parent process (PID: %d) is terminating.\n", getpid());
        
        free_linked_list(list);
        end = time(NULL);
    
        elapsed_time = difftime(end, start);
        printf("Elapsed time: %f seconds\n", elapsed_time);
    }
    return 0;
}