#include <stdio.h>
#include <stdlib.h>

struct element {
    struct element * previous ;
    int number ;
    struct element * next ;
};

struct element * insert ( int obj , struct element * ptr ) {
    struct element * p;
    p = ptr -> next;
    if ( p != NULL ) {
        p -> next = insert (obj , p);
    }
    else
    { 
        p = ( struct element *) malloc ( sizeof ( struct element ) );
        p -> number = obj;
        p -> next = NULL;
        p -> previous = ptr;
    }
    return p;
}

struct element * insertFront ( int obj , struct element * ptr ) {
    struct element * p;
    p = ptr -> next;
    if ( p != NULL ) {
        p -> previous = ( struct element *) malloc ( sizeof ( struct element ) );
        p = p -> previous;
        p -> number = obj;
        p -> next = ptr -> next;
        p -> previous = ptr;
    }
    else
    { 
        p = ( struct element *) malloc ( sizeof ( struct element ) );
        p -> number = obj;
        p -> next = NULL;
        p -> previous = ptr;
    }
    return p;
}

void delete(struct element * ptr, int index ) {
    if (ptr == NULL) {
        return;
    }

    struct element *temp = ptr;

    while (index-- && temp != NULL) {
        temp = temp->next;
    }

    if (temp == NULL) {
        return;
    }

    struct element *p = temp->previous;
    struct element *n = temp->next;

    if (p != NULL) {
        p->next = n;
    } else {
        ptr = n;
    }

    if (n != NULL) {
        n->previous = p;
    }

    free(temp);
}


struct element * innit_linked_list() {
    struct element * begin = ( struct element *) malloc ( sizeof ( struct element ) );
    begin -> next = NULL;
    begin -> previous = NULL;
    return begin;
}

void printList(struct element *list) {
    struct element *temp = list->next;
    while (temp != NULL) {
        printf("%d ", temp->number);
        temp = temp->next;
    }
    printf("\n");
}

void free_linked_list(struct element * list) {
    struct element *temp = list;
    while (temp != NULL) {
        struct element *nextNode = temp->next;
        free(temp);
        temp = nextNode;
    }
}

int main() {
    struct element * list = innit_linked_list();
    list->next = insert (1, list);
    list->next = insert (4, list);
    list->next = insert (2, list);
    printList(list);
    delete(list, 2);
    printList(list);
    list->next = insert (0, list);
    printList(list);
    free_linked_list(list);

    list = innit_linked_list();
    list->next = insert (1, list);
    printList(list);

    return 0;
}