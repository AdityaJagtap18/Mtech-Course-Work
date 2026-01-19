def matrix_chain_multiplication(dimensions):
    n = len(dimensions) - 1  # Number of matrices
    
    # Create tables for minimum cost and split points
    m = [[0] * n for _ in range(n)]  # Cost table
    k = [[0] * n for _ in range(n)]  # Split point table
    
    # L is chain length
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            m[i][j] = float('inf')
            
            # Try all possible split points
            for split in range(i, j):
                # Cost = left part + right part + merging cost
                cost = m[i][split] + m[split + 1][j] + \
                       dimensions[i] * dimensions[split + 1] * dimensions[j + 1]
                
                if cost < m[i][j]:
                    m[i][j] = cost
                    k[i][j] = split
    
    return m, k


def print_optimal_parenthesis(k, i, j, matrices):
    if i == j:
        print(matrices[i], end="")
    else:
        print("(", end="")
        print_optimal_parenthesis(k, i, k[i][j], matrices)
        print_optimal_parenthesis(k, k[i][j] + 1, j, matrices)
        print(")", end="")


# Input
print("=" * 60)
print("MATRIX CHAIN MULTIPLICATION - DYNAMIC PROGRAMMING")
print("=" * 60)

n = int(input("\nEnter number of matrices: "))
print("\nEnter dimensions (n+1 values):")
print("Example: For 3 matrices A1(10x20), A2(20x30), A3(30x40)")
print("Enter: 10 20 30 40")

dimensions = list(map(int, input("\nDimensions: ").split()))

# Generate matrix names
matrices = [f"A{i+1}" for i in range(n)]

# Compute tables
m, k = matrix_chain_multiplication(dimensions)

# Output
print("\n" + "=" * 60)
print("COST TABLE (m)")
print("=" * 60)
print("\nMinimum scalar multiplications needed:")
print("\n      ", end="")
for j in range(n):
    print(f"{j:^8}", end="")
print()
print("      " + "-" * (8 * n))

for i in range(n):
    print(f"{i:^6}|", end="")
    for j in range(n):
        if i <= j:
            print(f"{m[i][j]:^8}", end="")
        else:
            print(f"{'-':^8}", end="")
    print()

print("\n" + "=" * 60)
print("SPLIT POINT TABLE (k)")
print("=" * 60)
print("\nOptimal split positions:")
print("\n      ", end="")
for j in range(n):
    print(f"{j:^8}", end="")
print()
print("      " + "-" * (8 * n))

for i in range(n):
    print(f"{i:^6}|", end="")
    for j in range(n):
        if i < j:
            print(f"{k[i][j]:^8}", end="")
        else:
            print(f"{'-':^8}", end="")
    print()

print("\n" + "=" * 60)
print("MATRIX INFORMATION")
print("=" * 60)
for i in range(n):
    print(f"{matrices[i]}: {dimensions[i]} x {dimensions[i+1]}")

print("\n" + "=" * 60)
print("RESULT")
print("=" * 60)
print(f"\nMinimum number of scalar multiplications: {m[0][n-1]}")
print("\nOptimal Parenthesization: ", end="")
print_optimal_parenthesis(k, 0, n - 1, matrices)
print()
print("=" * 60)
