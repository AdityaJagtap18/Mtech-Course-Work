#include <iostream>
#include <chrono>
using namespace std;
using namespace chrono;

#define N 1024

float A[N][N], B[N][N], C[N][N];

void mat_mul() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
            for (int k = 0; k < N; k++)
                C[i][j] += A[i][k] * B[k][j];
        }
}

int main() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = rand() % 10;
            B[i][j] = rand() % 10;
        }

    auto t1 = high_resolution_clock::now();
    mat_mul();
    auto t2 = high_resolution_clock::now();

    cout << "Matrix Multiply (" << N << "x" << N << ")\n"
         << "Time : " << duration<double, milli>(t2 - t1).count() << " ms\n";

    return 0;
}
