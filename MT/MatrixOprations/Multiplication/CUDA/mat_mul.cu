#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cuda_runtime.h>

#define TILE_SIZE 16
#define N 1024

// ─────────────────────────────────────────────
// Naive Kernel: C = A * B
// ─────────────────────────────────────────────
__global__ void mat_mul_naive(float *A, float *B, float *C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        float sum = 0.0f;
        for (int k = 0; k < n; k++)
            sum += A[row * n + k] * B[k * n + col];
        C[row * n + col] = sum;
    }
}

// ─────────────────────────────────────────────
// Tiled Kernel: C = A * B (shared memory)
// ─────────────────────────────────────────────
__global__ void mat_mul_tiled(float *A, float *B, float *C, int n) {
    __shared__ float sA[TILE_SIZE][TILE_SIZE];
    __shared__ float sB[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < (n + TILE_SIZE - 1) / TILE_SIZE; t++) {
        sA[threadIdx.y][threadIdx.x] = (row < n && t * TILE_SIZE + threadIdx.x < n)
            ? A[row * n + t * TILE_SIZE + threadIdx.x] : 0.0f;

        sB[threadIdx.y][threadIdx.x] = (col < n && t * TILE_SIZE + threadIdx.y < n)
            ? B[(t * TILE_SIZE + threadIdx.y) * n + col] : 0.0f;

        __syncthreads();

        for (int k = 0; k < TILE_SIZE; k++)
            sum += sA[threadIdx.y][k] * sB[k][threadIdx.x];

        __syncthreads();
    }

    if (row < n && col < n)
        C[row * n + col] = sum;
}

// ─────────────────────────────────────────────
// CPU Reference
// ─────────────────────────────────────────────
void cpu_mul(float *A, float *B, float *C, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            float sum = 0.0f;
            for (int k = 0; k < n; k++)
                sum += A[i * n + k] * B[k * n + j];
            C[i * n + j] = sum;
        }
}

// ─────────────────────────────────────────────
// Verify
// ─────────────────────────────────────────────
bool verify(float *ref, float *gpu, int n, float tol = 1e-2f) {
    for (int i = 0; i < n * n; i++)
        if (fabs(ref[i] - gpu[i]) > tol) {
            printf("  Mismatch at [%d]: CPU=%.5f  GPU=%.5f\n", i, ref[i], gpu[i]);
            return false;
        }
    return true;
}

int main() {
    size_t bytes = N * N * sizeof(float);

    printf("===========================================\n");
    printf("  CUDA Matrix Multiply  C = A * B (%dx%d)\n", N, N);
    printf("===========================================\n\n");

    // ── Host memory ──
    float *hA = (float*)malloc(bytes);
    float *hB = (float*)malloc(bytes);
    float *hC = (float*)malloc(bytes);

    for (int i = 0; i < N * N; i++) {
        hA[i] = (float)rand() / RAND_MAX;
        hB[i] = (float)rand() / RAND_MAX;
    }

    // ── Device memory ──
    float *dA, *dB, *dC;
    cudaMalloc(&dA, bytes);
    cudaMalloc(&dB, bytes);
    cudaMalloc(&dC, bytes);
    cudaMemcpy(dA, hA, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(dB, hB, bytes, cudaMemcpyHostToDevice);

    dim3 threads(TILE_SIZE, TILE_SIZE);
    dim3 blocks((N + TILE_SIZE - 1) / TILE_SIZE, (N + TILE_SIZE - 1) / TILE_SIZE);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    float ms;

    // ── Naive ──
    printf("[ Naive Kernel ]\n");
    cudaEventRecord(start);
    mat_mul_naive<<<blocks, threads>>>(dA, dB, dC, N);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms, start, stop);
    printf("  GPU Time : %.3f ms\n\n", ms);

    // ── Tiled ──
    printf("[ Tiled Kernel (shared memory) ]\n");
    cudaEventRecord(start);
    mat_mul_tiled<<<blocks, threads>>>(dA, dB, dC, N);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms, start, stop);
    printf("  GPU Time : %.3f ms\n", ms);
    cudaMemcpy(hC, dC, bytes, cudaMemcpyDeviceToHost);

    // ── Verify on small matrix ──
    int Ns = 256;
    size_t sb = Ns * Ns * sizeof(float);
    float *cA = (float*)malloc(sb), *cB = (float*)malloc(sb);
    float *cC = (float*)malloc(sb), *gC = (float*)malloc(sb);
    for (int i = 0; i < Ns * Ns; i++) { cA[i] = hA[i]; cB[i] = hB[i]; }

    float *dA2, *dB2, *dC2;
    cudaMalloc(&dA2, sb); cudaMalloc(&dB2, sb); cudaMalloc(&dC2, sb);
    cudaMemcpy(dA2, cA, sb, cudaMemcpyHostToDevice);
    cudaMemcpy(dB2, cB, sb, cudaMemcpyHostToDevice);

    dim3 b2((Ns+TILE_SIZE-1)/TILE_SIZE, (Ns+TILE_SIZE-1)/TILE_SIZE);
    mat_mul_tiled<<<b2, threads>>>(dA2, dB2, dC2, Ns);
    cudaMemcpy(gC, dC2, sb, cudaMemcpyDeviceToHost);
    cpu_mul(cA, cB, cC, Ns);

    printf("  Verify   : %s\n", verify(cC, gC, Ns) ? "PASSED ✓" : "FAILED ✗");

    // ── Cleanup ──
    cudaFree(dA); cudaFree(dB); cudaFree(dC);
    cudaFree(dA2); cudaFree(dB2); cudaFree(dC2);
    free(hA); free(hB); free(hC);
    free(cA); free(cB); free(cC); free(gC);
    cudaEventDestroy(start); cudaEventDestroy(stop);

    return 0;
}
