// Bubble Sort using OpenMP in C++
// Compile: g++ -fopenmp bubble_sort_openmp.cpp -o bubble_sort_openmp
// Run:     ./bubble_sort_openmp

#include <iostream>
#include <omp.h>
using namespace std;

// Function to print array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;
}

// Bubble Sort using OpenMP (Odd-Even approach)
// Normal bubble sort can't be parallelized directly
// so we use Odd-Even transposition sort with OpenMP
void bubbleSortOpenMP(int arr[], int n) {
    for (int i = 0; i < n; i++) {

        // Even phase: compare (0,1), (2,3), (4,5) ...
        #pragma omp parallel for num_threads(4)
        for (int j = 0; j < n - 1; j += 2) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }

        // Odd phase: compare (1,2), (3,4), (5,6) ...
        #pragma omp parallel for num_threads(4)
        for (int j = 1; j < n - 1; j += 2) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Before sorting: ";
    printArray(arr, n);

    double start = omp_get_wtime();       // start timer

    bubbleSortOpenMP(arr, n);

    double end = omp_get_wtime();         // end timer

    cout << "After sorting:  ";
    printArray(arr, n);

    cout << "Time taken: " << (end - start) << " seconds\n";

    return 0;
}
