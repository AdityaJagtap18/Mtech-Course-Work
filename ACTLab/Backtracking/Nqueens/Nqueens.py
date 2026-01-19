def is_safe(board, row, col, n):
    # Check column
    for i in range(row):
        if board[i][col] == 1:
            return False
    
    # Check upper left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    
    # Check upper right diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    
    return True


def solve_n_queens(board, row, n, solutions):
    # Base case: All queens placed
    if row == n:
        # Store the solution
        solution = [row[:] for row in board]
        solutions.append(solution)
        return
    
    # Try placing queen in each column of current row
    for col in range(n):
        if is_safe(board, row, col, n):
            # Place queen
            board[row][col] = 1
            
            # Recurse for next row
            solve_n_queens(board, row + 1, n, solutions)
            
            # Backtrack: Remove queen
            board[row][col] = 0


def print_solution(board, n, solution_num):
    print(f"\nSolution {solution_num}:")
    print("-" * (4 * n + 1))
    for i in range(n):
        print("|", end=" ")
        for j in range(n):
            if board[i][j] == 1:
                print("Q", end=" | ")
            else:
                print(".", end=" | ")
        print()
        print("-" * (4 * n + 1))


# Input
print("=" * 50)
print("N-QUEENS PROBLEM - BACKTRACKING")
print("=" * 50)

n = int(input("\nEnter the value of N: "))

# Initialize board
board = [[0] * n for _ in range(n)]
solutions = []

# Solve
solve_n_queens(board, 0, n, solutions)

# Output
print("\n" + "=" * 50)
print("RESULTS")
print("=" * 50)

if len(solutions) == 0:
    print("\nNo solution exists!")
else:
    print(f"\nTotal number of solutions: {len(solutions)}")
    
    for idx, solution in enumerate(solutions, 1):
        print_solution(solution, n, idx)

print("\n" + "=" * 50)
print(f"Total solutions found: {len(solutions)}")
print("=" * 50)
