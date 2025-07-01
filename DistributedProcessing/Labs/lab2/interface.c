#include <stdio.h>
#include "linked_list.h"

void printMenu() {
    printf("\nChoose action:\n");
    printf(" 1 - print whole list\n");
    printf(" 2 - delete whole list\n");
    printf(" 3 - delete elements\n");
    printf(" 4 - insert element to list\n");
    printf(" 5 - to exit program\n:");
}

int main() {
    int input;
    int command;
    int out = 0;
    struct element * list = innit_linked_list();
    while (1) {
        printMenu();
        scanf("%d", &command);
        switch (command) {
            case 1 :
                printList(list);
                break;
            case 2 :
                free_linked_list(list);
                break;
            case 3 :
                printf("Give number of element to delete:");
                scanf("%d", &input);
                delete(list, input);
                break;
            case 4 :
                printf("Give element to insert:");
                scanf("%d", &input);
                list->next = insert (input, list);
                break;
            default :
                out = 1;
        }
        if (out == 1)
            break;
    }
    free_linked_list(list);
    return 0;
}