#include <iostream>
#include <chrono>
#include <pthread.h>
using namespace std;
using namespace chrono;

#define N       1024
#define THREADS 8

float A[N][N], B[N][N], C[N][N];

void* worker(void* arg) {
    int t = *(int*)arg;
    int rows = N / THREADS;
    int start = t * rows;
    int end   = (t == THREADS - 1) ? N : start + rows;

    for (int i = start; i < end; i++)
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
            for (int k = 0; k < N; k++)
                C[i][j] += A[i][k] * B[k][j];
        }

    return nullptr;
}

int main() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            A[i][j] = rand() % 10;
            B[i][j] = rand() % 10;
        }

    pthread_t tid[THREADS];
    int ids[THREADS];

    auto t1 = high_resolution_clock::now();
    for (int t = 0; t < THREADS; t++) { ids[t] = t; pthread_create(&tid[t], nullptr, worker, &ids[t]); }
    for (int t = 0; t < THREADS; t++) pthread_join(tid[t], nullptr);
    auto t2 = high_resolution_clock::now();

    cout << "Matrix Multiply (" << N << "x" << N << ")\n"
         << "Threads : " << THREADS << "\n"
         << "Time    : " << duration<double, milli>(t2 - t1).count() << " ms\n";

    return 0;
}
