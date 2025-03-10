#include <stdbool.h>
#define SIZE 9

extern "C" {
    bool is_empty(int* board, int x, int y) {
        return *(board + x * SIZE + y) == 0;
    }

    bool is_on_edge(int x, int y) {
        return (x == 0 || x == SIZE - 1 || y == 0 || y == SIZE - 1);
    }
}
