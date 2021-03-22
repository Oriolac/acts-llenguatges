#include "prova2.c"
#define func(a, b, c) a < b && b < c

int main() {
    if(func(1, 2, 3)) {
        printf("HELLO\n");
    }
    printf("NO");
}
