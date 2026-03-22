// Bubble Sort using CUDA (Odd-Even Transposition Sort)
// Compile: nvcc bubble_sort_cuda.cu -o bubble_sort_cuda
// Run:     ./bubble_sort_cuda

#include <iostream>
#include <cuda.h>
using namespace std;

#define N 10  // array size

// ── CUDA Kernel: Even Phase ──────────────────────────────────────────────────
__global__ void evenPhase(int* arr, int n) {
    int j = (blockIdx.x * blockDim.x + threadIdx.x) * 2;  // 0, 2, 4, 6 ...

    if (j < n - 1) {
        if (arr[j] > arr[j + 1]) {
            // swap
            int temp  = arr[j];
            arr[j]    = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}

// ── CUDA Kernel: Odd Phase ───────────────────────────────────────────────────
__global__ void oddPhase(int* arr, int n) {
    int j = (blockIdx.x * blockDim.x + threadIdx.x) * 2 + 1;  // 1, 3, 5, 7 ...

    if (j < n - 1) {
        if (arr[j] > arr[j + 1]) {
            // swap
            int temp   = arr[j];
            arr[j]     = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}

// ── Helper: Print Array ──────────────────────────────────────────────────────
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;
}

// ── Main ─────────────────────────────────────────────────────────────────────
int main() {
    int h_arr[N] = {64, 34, 25, 12, 22, 11, 90, 45, 78, 5};  // host array

    cout << "Before sorting: ";
    printArray(h_arr, N);

    // ── Allocate memory on GPU ───────────────────────────────────────────────
    int* d_arr;
    cudaMalloc((void**)&d_arr, N * sizeof(int));

    // ── Copy array from CPU to GPU ───────────────────────────────────────────
    cudaMemcpy(d_arr, h_arr, N * sizeof(int), cudaMemcpyHostToDevice);

    // ── Launch kernels N times (each pass = 1 even + 1 odd phase) ───────────
    int threads = 256;
    int blocks  = (N / 2 + threads - 1) / threads;  // enough blocks to cover array

    for (int i = 0; i < N; i++) {
        evenPhase<<<blocks, threads>>>(d_arr, N);  // even phase
        cudaDeviceSynchronize();                   // wait for all threads

        oddPhase<<<blocks, threads>>>(d_arr, N);   // odd phase
        cudaDeviceSynchronize();                   // wait for all threads
    }

    // ── Copy sorted array back from GPU to CPU ───────────────────────────────
    cudaMemcpy(h_arr, d_arr, N * sizeof(int), cudaMemcpyDeviceToHost);

    cout << "After sorting:  ";
    printArray(h_arr, N);

    // ── Free GPU memory ──────────────────────────────────────────────────────
    cudaFree(d_arr);

    return 0;
}
