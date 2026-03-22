// Bubble Sort using Pthreads in C++
// Compile: g++ bubble_sort_pthreads.cpp -o bubble_sort_pthreads -lpthread
// Run:     ./bubble_sort_pthreads

#include <iostream>
#include <pthread.h>
using namespace std;

#define NUM_THREADS 4

int arr[] = {64, 34, 25, 12, 22, 11, 90, 45, 78, 5};
int n = 10;

pthread_barrier_t barrier;  // to sync threads between odd/even phases

// Struct to pass data to each thread
struct ThreadData {
    int tid;
    int phase;  // 0 = even phase, 1 = odd phase
};

// Function to print array
void printArray() {
    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;
}

// Thread function: does one phase (even or odd) of odd-even sort
void* oddEvenPhase(void* arg) {
    int tid = *(int*)arg;

    for (int i = 0; i < n; i++) {

        // Even phase: compare (0,1), (2,3), (4,5) ...
        for (int j = tid * 2; j < n - 1; j += NUM_THREADS * 2) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }

        pthread_barrier_wait(&barrier);  // wait for all threads to finish even phase

        // Odd phase: compare (1,2), (3,4), (5,6) ...
        for (int j = tid * 2 + 1; j < n - 1; j += NUM_THREADS * 2) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }

        pthread_barrier_wait(&barrier);  // wait for all threads to finish odd phase
    }

    return nullptr;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int tids[NUM_THREADS];

    cout << "Before sorting: ";
    printArray();

    // Init barrier: releases when all NUM_THREADS threads reach it
    pthread_barrier_init(&barrier, nullptr, NUM_THREADS);

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        tids[i] = i;
        pthread_create(&threads[i], nullptr, oddEvenPhase, &tids[i]);
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], nullptr);
    }

    cout << "After sorting:  ";
    printArray();

    pthread_barrier_destroy(&barrier);

    return 0;
}
