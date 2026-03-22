// Compile: g++ -fopenmp openmp_demo.cpp -o openmp_demo
// Run:     ./openmp_demo

#include <iostream>
#include <omp.h>

// ── Simple semaphore built from OpenMP lock ──────────────────────────────────
// OpenMP has no built-in semaphore, so we mimic one with a counter + lock.

int semaphore_count = 1;        // 1 = binary semaphore (mutex-like)
omp_lock_t sem_lock;

void sem_wait() {
    while (true) {
        omp_set_lock(&sem_lock);
        if (semaphore_count > 0) {
            semaphore_count--;          // acquire
            omp_unset_lock(&sem_lock);
            break;
        }
        omp_unset_lock(&sem_lock);
        // busy-wait; in real code you'd yield/sleep
    }
}

void sem_post() {
    omp_set_lock(&sem_lock);
    semaphore_count++;                  // release
    omp_unset_lock(&sem_lock);
}

// ── Shared resource protected by semaphore ───────────────────────────────────
int shared_counter = 0;

int main() {
    omp_init_lock(&sem_lock);

    std::cout << "=== OpenMP Demo: Semaphore + Barrier ===\n\n";

    // ── PART 1: Semaphore ────────────────────────────────────────────────────
    std::cout << "-- Semaphore section --\n";

    #pragma omp parallel num_threads(4)
    {
        int tid = omp_get_thread_num();

        sem_wait();                     // enter critical section
        shared_counter++;
        std::cout << "Thread " << tid
                  << " incremented counter to " << shared_counter << "\n";
        sem_post();                     // leave critical section
    }

    std::cout << "Final counter value: " << shared_counter << "\n\n";

    // ── PART 2: Barrier ──────────────────────────────────────────────────────
    std::cout << "-- Barrier section --\n";

    #pragma omp parallel num_threads(4)
    {
        int tid = omp_get_thread_num();

        // Phase 1: each thread does some work
        std::cout << "Thread " << tid << " doing phase-1 work\n";

        #pragma omp barrier     // all threads wait here before proceeding

        // Phase 2: only starts after ALL threads finish phase 1
        std::cout << "Thread " << tid << " doing phase-2 work\n";
    }

    omp_destroy_lock(&sem_lock);
    std::cout << "\nDone.\n";
    return 0;
}
