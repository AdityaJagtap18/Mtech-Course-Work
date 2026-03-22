// Compile: g++ pthreads_demo.cpp -o pthreads_demo -lpthread
// Run:     ./pthreads_demo

#include <iostream>
#include <pthread.h>
#include <semaphore.h>   // POSIX semaphore

// ── Globals ──────────────────────────────────────────────────────────────────
#define NUM_THREADS 4

// Semaphore
sem_t semaphore;
int shared_counter = 0;

// Barrier
pthread_barrier_t barrier;

// ── Thread function ──────────────────────────────────────────────────────────
void* thread_func(void* arg) {
    int tid = *(int*)arg;

    // ── PART 1: Semaphore ────────────────────────────────────────────────────
    sem_wait(&semaphore);               // acquire (blocks if count == 0)

    shared_counter++;
    std::cout << "Thread " << tid
              << " incremented counter to " << shared_counter << "\n";

    sem_post(&semaphore);               // release

    // ── PART 2: Barrier ──────────────────────────────────────────────────────
    std::cout << "Thread " << tid << " reached the barrier\n";

    pthread_barrier_wait(&barrier);     // wait until ALL threads arrive here

    std::cout << "Thread " << tid << " passed the barrier\n";

    return nullptr;
}

// ── Main ─────────────────────────────────────────────────────────────────────
int main() {
    std::cout << "=== Pthreads Demo: Semaphore + Barrier ===\n\n";

    pthread_t threads[NUM_THREADS];
    int tids[NUM_THREADS];

    // Init semaphore: initial value 1 → only one thread at a time
    sem_init(&semaphore, 0, 1);

    // Init barrier: releases when NUM_THREADS threads are waiting
    pthread_barrier_init(&barrier, nullptr, NUM_THREADS);

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        tids[i] = i;
        pthread_create(&threads[i], nullptr, thread_func, &tids[i]);
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], nullptr);
    }

    std::cout << "\nFinal counter value: " << shared_counter << "\n";

    // Cleanup
    sem_destroy(&semaphore);
    pthread_barrier_destroy(&barrier);

    std::cout << "Done.\n";
    return 0;
}
