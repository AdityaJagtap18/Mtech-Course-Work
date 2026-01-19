def tsp(cost, n, pos, visited, memo):
    # Base case: All cities visited, return cost to go back to start
    if visited == (1 << n) - 1:
        return cost[pos][0]
    
    # Check if already computed
    if memo[pos][visited] != -1:
        return memo[pos][visited]
    
    min_cost = float('inf')
    
    # Try visiting all unvisited cities
    for city in range(n):
        if visited & (1 << city) == 0:  # If city not visited
            new_cost = cost[pos][city] + tsp(cost, n, city, visited | (1 << city), memo)
            min_cost = min(min_cost, new_cost)
    
    memo[pos][visited] = min_cost
    return min_cost


# Input
print("=" * 50)
print("TRAVELING SALESMAN PROBLEM - DYNAMIC PROGRAMMING")
print("=" * 50)

n = int(input("\nEnter number of cities: "))
print("\nEnter cost matrix:")

cost = []
for i in range(n):
    row = list(map(int, input(f"Row {i}: ").split()))
    cost.append(row)

# Memoization table
memo = [[-1] * (1 << n) for _ in range(n)]

# Start from city 0 with only city 0 visited
result = tsp(cost, n, 0, 1, memo)

# Output
print("\n" + "=" * 50)
print("RESULT")
print("=" * 50)
print(f"\nMinimum cost to complete the tour: {result}")
print("=" * 50)
