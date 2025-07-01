#include <stdio.h>
#include <stdlib.h>

struct table {
    int Id;
    char Town[20];
    int Population;
    float Latitude;
    float Longitude;
};

struct Node {
    int *permutation;
    int length;
    int numChildren;
    struct Node **children;
};

int contains(int *permutation, int length, int number) {
    for (int i = 0; i < length; i++) {
        if (permutation[i] == number) return 1;
    }
    return 0;
}

struct Node* createNode(int *permutation, int length, int n) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->permutation = (int*)malloc(length * sizeof(int));
    
    for(int i = 0; i < length; i++) {
        newNode->permutation[i] = permutation[i];
    }

    newNode->length = length;
    newNode->numChildren = (length < n) ? (n - length) : 0; 
    newNode->children = (struct Node**)malloc(newNode->numChildren * sizeof(struct Node*));

    return newNode;
}

struct Node* buildTree(int permutation[], int length, int n) {
    struct Node* root = createNode(permutation, length, n);

    if (length == n) return root;

    int childIndex = 0; 
    for (int i = 1; i <= n; i++) {
        if (!contains(permutation, length, i)) {
            int* newPermutation = (int*)malloc((length + 1) * sizeof(int));
            for (int j = 0; j < length; j++) {
                newPermutation[j] = permutation[j];
            }
            newPermutation[length] = i;

            root->children[childIndex] = buildTree(newPermutation, length + 1, n);
            childIndex++;

            free(newPermutation);
        }
    }

    return root;
}

void printTree(struct Node* tree, int n) {
    if (tree == NULL) return;

    if (tree->length == n) {
        for (int i = 0; i < tree->length; i++) {
            printf("%d ", tree->permutation[i]);
        }
        printf("\n");
    }

    for (int i = 0; i < tree->numChildren; i++) {
        printTree(tree->children[i], n);
    }
}

void freeTree(struct Node* tree) {
    if (tree == NULL) return;

    for (int i = 0; i < tree->numChildren; i++) {
        freeTree(tree->children[i]);
    }

    free(tree->permutation);
    free(tree->children);
    free(tree);
}

void printCombination(int set[], int k) {
    for (int i = 0; i < k; i++) {
        printf("%d ", set[i]);
    }
    printf("\n");
}

void combination(int set[], int n, int k) {
    while(1) {
        printCombination(set, k);
        int current = k-1;
        while (current >= 0 && set[current] == n - (k - 1 - current)) {
            current--;
        }
        
        if (current < 0) break;
        set[current] += 1;

        for (int i = current+1; i < k; i++) {
            set[i] = set[i-1]+1;
        }
    }
}

int main() {
    int n = 6;
    struct table cities[15];

    FILE* file;
    file = fopen("france.txt", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    int count = 0;
    while (count < n && fscanf(file, "%d %s %d %f %f", &cities[count].Id, cities[count].Town,
              &cities[count].Population, &cities[count].Latitude, &cities[count].Longitude)) {
        count++;
    }

    int *permutation = (int*)malloc(0);

    struct Node* tree = buildTree(permutation, 0, n);
    //printTree(tree, n);

    freeTree(tree);

    int *set = (int*)malloc(n * sizeof(int));

    int k = 4;
    for (int i = 0; i < k; i++) {
        set[i] = i+1;
    }

    combination(set, n, k);

    fclose(file);
    return 0;
}