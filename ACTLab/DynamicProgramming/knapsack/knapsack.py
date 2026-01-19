def knapsack(weights, profits, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(profits[i-1] + dp[i-1][w - weights[i-1]], 
                               dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtrack to find selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    selected_items.reverse()
    return dp[n][capacity], selected_items


# Input
print("=" * 50)
print("0/1 KNAPSACK PROBLEM - DYNAMIC PROGRAMMING")
print("=" * 50)

n = int(input("\nEnter number of items: "))
weights = list(map(int, input("Enter weights (space-separated): ").split()))
profits = list(map(int, input("Enter profits (space-separated): ").split()))
capacity = int(input("Enter bag capacity: "))

# Process
max_profit, selected = knapsack(weights, profits, capacity)

# Output
print("\n" + "=" * 50)
print("RESULTS")
print("=" * 50)

print(f"\nMaximum Profit: {max_profit}")
print(f"\nSelected Items (0-indexed):")
print("-" * 50)
print(f"{'Item':<10}{'Weight':<15}{'Profit':<15}")
print("-" * 50)

total_weight = 0
for idx in selected:
    print(f"{idx:<10}{weights[idx]:<15}{profits[idx]:<15}")
    total_weight += weights[idx]

print("-" * 50)
print(f"{'Total':<10}{total_weight:<15}{max_profit:<15}")
print(f"\nCapacity Used: {total_weight}/{capacity}")
print("=" * 50)
