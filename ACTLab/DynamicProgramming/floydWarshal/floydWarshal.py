def floyd_warshall(graph):
    n = len(graph)
    # Create distance matrix (copy of graph)
    dist = [[graph[i][j] for j in range(n)] for i in range(n)]
    
    # Floyd Warshall Algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist


# Input
print("=" * 60)
print("FLOYD WARSHALL'S ALGORITHM - ALL PAIRS SHORTEST PATH")
print("=" * 60)

n = int(input("\nEnter number of nodes: "))
print("\nEnter adjacency matrix (use 999999 for infinity):")
print("Enter each row (space-separated):")

graph = []
for i in range(n):
    row = list(map(int, input(f"Row {i}: ").split()))
    graph.append(row)

# Process
result = floyd_warshall(graph)

# Output
print("\n" + "=" * 60)
print("INPUT GRAPH (Adjacency Matrix)")
print("=" * 60)
print("\n     ", end="")
for j in range(n):
    print(f"{j:^8}", end="")
print()
print("     " + "-" * (8 * n))

for i in range(n):
    print(f"{i:^5}|", end="")
    for j in range(n):
        if graph[i][j] == 999999:
            print(f"{'INF':^8}", end="")
        else:
            print(f"{graph[i][j]:^8}", end="")
    print()

print("\n" + "=" * 60)
print("SHORTEST DISTANCE MATRIX")
print("=" * 60)
print("\n     ", end="")
for j in range(n):
    print(f"{j:^8}", end="")
print()
print("     " + "-" * (8 * n))

for i in range(n):
    print(f"{i:^5}|", end="")
    for j in range(n):
        if result[i][j] == 999999:
            print(f"{'INF':^8}", end="")
        else:
            print(f"{result[i][j]:^8}", end="")
    print()

print("\n" + "=" * 60)
print("ALL PAIRS SHORTEST PATHS")
print("=" * 60)

for i in range(n):
    for j in range(n):
        if i != j:
            if result[i][j] == 999999:
                print(f"Node {i} to Node {j}: No path exists")
            else:
                print(f"Node {i} to Node {j}: {result[i][j]}")

print("=" * 60)
