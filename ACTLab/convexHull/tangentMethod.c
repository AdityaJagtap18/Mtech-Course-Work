#include <stdio.h>
#include <stdlib.h>

typedef struct Point {
    int x, y;
} Point;

int cross(Point O, Point A, Point B) {
    return (A.x - O.x) * (B.y - O.y) -
           (A.y - O.y) * (B.x - O.x);
}

Point* mergeHulls(Point *leftHull, int leftSize, Point *rightHull, int rightSize, int *mergedSize) {
    int i, j;

    i = 0;
    for (int k = 1; k < leftSize; k++) {
        if (leftHull[k].x > leftHull[i].x)
            i = k;
    }

    j = 0;
    for (int k = 1; k < rightSize; k++) {
        if (rightHull[k].x < rightHull[j].x)
            j = k;
    }

    int done = 0;
    int i_upper = i, j_upper = j;
    while (!done) {
        done = 1;
        while (cross(rightHull[j_upper], leftHull[i_upper], leftHull[(i_upper+1)%leftSize]) >= 0)
            i_upper = (i_upper+1) % leftSize;
        while (cross(leftHull[i_upper], rightHull[j_upper], rightHull[(j_upper-1+rightSize)%rightSize]) <= 0) {
            j_upper = (j_upper-1+rightSize) % rightSize;
            done = 0;
        }
    }

    done = 0;
    int i_lower = i, j_lower = j;
    while (!done) {
        done = 1;
        while (cross(rightHull[j_lower], leftHull[i_lower], leftHull[(i_lower-1+leftSize)%leftSize]) <= 0)
            i_lower = (i_lower-1+leftSize) % leftSize;
        while (cross(leftHull[i_lower], rightHull[j_lower], rightHull[(j_lower+1)%rightSize]) >= 0) {
            j_lower = (j_lower+1) % rightSize;
            done = 0;
        }
    }
}