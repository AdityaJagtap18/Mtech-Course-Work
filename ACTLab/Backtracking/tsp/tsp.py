import sys

class Node:
    def __init__(self, path, reduced_matrix, cost, level):
        self.path = path
        self.reduced_matrix = [row[:] for row in reduced_matrix]
        self.cost = cost
        self.level = level


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def reduce_matrix(matrix, n):
    cost = 0
    
    # Row reduction
    for i in range(n):
        min_val = min(matrix[i])
        if min_val != float('inf') and min_val > 0:
            cost += min_val
            for j in range(n):
                if matrix[i][j] != float('inf'):
                    matrix[i][j] -= min_val
    
    # Column reduction
    for j in range(n):
        min_val = min(matrix[i][j] for i in range(n))
        if min_val != float('inf') and min_val > 0:
            cost += min_val
            for i in range(n):
                if matrix[i][j] != float('inf'):
                    matrix[i][j] -= min_val
    
    return cost


def calculate_cost(parent_node, i, j, n):
    # Create new matrix
    matrix = copy_matrix(parent_node.reduced_matrix)
    
    # Set all values in row i and column j to infinity
    for k in range(n):
        matrix[i][k] = float('inf')
        matrix[k][j] = float('inf')
    
    # Set matrix[j][0] to infinity (prevent premature return to start)
    matrix[j][0] = float('inf')
    
    # Reduce the matrix and calculate cost
    reduction_cost = reduce_matrix(matrix, n)
    
    total_cost = parent_node.cost + parent_node.reduced_matrix[i][j] + reduction_cost
    
    return total_cost, matrix


def tsp_branch_bound(cost_matrix, n):
    # Priority queue (min-heap simulation with list)
    pq = []
    
    # Create root node
    initial_matrix = copy_matrix(cost_matrix)
    root_cost = reduce_matrix(initial_matrix, n)
    root = Node([0], initial_matrix, root_cost, 0)
    
    pq.append(root)
    min_cost = float('inf')
    best_path = []
    
    nodes_explored = 0
    
    while pq:
        # Get node with minimum cost
        pq.sort(key=lambda x: x.cost)
        min_node = pq.pop(0)
        
        nodes_explored += 1
        i = min_node.path[-1]
        
        # If all cities visited
        if min_node.level == n - 1:
            # Add cost to return to start
            final_cost = min_node.cost + cost_matrix[i][0]
            if final_cost < min_cost:
                min_cost = final_cost
                best_path = min_node.path + [0]
            continue
        
        # For each unvisited city
        for j in range(n):
            if j not in min_node.path:
                # Calculate cost and reduced matrix
                new_cost, new_matrix = calculate_cost(min_node, i, j, n)
                
                # Only add to queue if cost is promising
                if new_cost < min_cost:
                    new_path = min_node.path + [j]
                    new_node = Node(new_path, new_matrix, new_cost, min_node.level + 1)
                    pq.append(new_node)
    
    return best_path, min_cost, nodes_explored


def print_matrix(matrix, n):
    print("\n     ", end="")
    for j in range(n):
        print(f"{j:^8}", end="")
    print()
    print("     " + "-" * (8 * n))
    
    for i in range(n):
        print(f"{i:^5}|", end="")
        for j in range(n):
            if matrix[i][j] == float('inf'):
                print(f"{'INF':^8}", end="")
            else:
                print(f"{matrix[i][j]:^8}", end="")
        print()


# Input
print("=" * 60)
print("TRAVELING SALESMAN PROBLEM - BRANCH AND BOUND")
print("=" * 60)

n = int(input("\nEnter number of cities: "))
print("\nEnter cost matrix (use 9999 for no direct path):")

cost_matrix = []
for i in range(n):
    row = list(map(int, input(f"Row {i}: ").split()))
    # Convert 9999 to infinity
    row = [float('inf') if x == 9999 else x for x in row]
    cost_matrix.append(row)

# Solve TSP
best_path, min_cost, nodes_explored = tsp_branch_bound(cost_matrix, n)

# Output
print("\n" + "=" * 60)
print("INPUT COST MATRIX")
print("=" * 60)
print_matrix(cost_matrix, n)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

if best_path:
    print(f"\nMinimum Cost: {min_cost}")
    print(f"\nOptimal Path: ", end="")
    for i in range(len(best_path)):
        if i > 0:
            print(" -> ", end="")
        print(best_path[i], end="")
    
    print("\n\nDetailed Route:")
    print("-" * 40)
    total = 0
    for i in range(len(best_path) - 1):
        from_city = best_path[i]
        to_city = best_path[i + 1]
        edge_cost = cost_matrix[from_city][to_city]
        total += edge_cost
        print(f"City {from_city} -> City {to_city}: {edge_cost}")
    print("-" * 40)
    print(f"Total Cost: {total}")
    
    print(f"\nNodes Explored: {nodes_explored}")
else:
    print("\nNo solution found!")

print("\n" + "=" * 60)