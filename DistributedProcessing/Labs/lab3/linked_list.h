struct element {
    struct element * previous ;
    int number ;
    struct element * next ;
};

struct element * insert ( int obj , struct element * ptr );

struct element * insertFront ( int obj , struct element * ptr );

void delete(struct element * ptr, int index );

struct element * innit_linked_list();

void printList(struct element *list);

void free_linked_list(struct element * list);