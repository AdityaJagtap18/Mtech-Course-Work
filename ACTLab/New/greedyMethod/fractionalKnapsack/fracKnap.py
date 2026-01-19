#!/usr/bin/env python3
"""
Fractional Knapsack Problem using Greedy Method
"""

class Item:
    """Class to represent an item with weight and value"""
    def __init__(self, weight, value, index):
        self.weight = weight
        self.value = value
        self.index = index
        self.ratio = value / weight  # value per unit weight
    
    def __repr__(self):
        return f"Item{self.index}(w={self.weight}, v={self.value}, ratio={self.ratio:.2f})"


def fractional_knapsack(weights, values, capacity):
    """
    Solve fractional knapsack problem using greedy method
    
    Args:
        weights: list of item weights
        values: list of item values
        capacity: maximum weight capacity of knapsack
    
    Returns:
        max_value: maximum value achievable
        selected_items: list of (item_index, fraction_taken)
    """
    n = len(weights)
    
    # Create items with their ratios
    items = []
    for i in range(n):
        items.append(Item(weights[i], values[i], i))
    
    # Sort items by value-to-weight ratio in descending order (Greedy choice)
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    max_value = 0.0
    selected_items = []
    remaining_capacity = capacity
    
    print("\nGreedy Selection Process:")
    print("-" * 70)
    print(f"{'Item':<10} {'Weight':<10} {'Value':<10} {'Ratio':<10} {'Taken':<15} {'Value Added':<15}")
    print("-" * 70)
    
    for item in items:
        if remaining_capacity == 0:
            break
        
        if item.weight <= remaining_capacity:
            # Take the whole item
            fraction_taken = 1.0
            value_added = item.value
            remaining_capacity -= item.weight
        else:
            # Take fractional part
            fraction_taken = remaining_capacity / item.weight
            value_added = item.value * fraction_taken
            remaining_capacity = 0
        
        max_value += value_added
        selected_items.append((item.index, fraction_taken))
        
        print(f"Item {item.index:<5} {item.weight:<10} {item.value:<10} "
              f"{item.ratio:<10.2f} {fraction_taken:<15.2%} {value_added:<15.2f}")
    
    print("-" * 70)
    
    return max_value, selected_items


def display_solution(weights, values, capacity, max_value, selected_items):
    """Display the solution in a clear format"""
    print("\n" + "=" * 70)
    print("FRACTIONAL KNAPSACK SOLUTION")
    print("=" * 70)
    
    print(f"\nKnapsack Capacity: {capacity}")
    print(f"Maximum Value Achieved: {max_value:.2f}")
    
    print("\nItems taken:")
    total_weight = 0
    for item_idx, fraction in selected_items:
        weight_taken = weights[item_idx] * fraction
        value_taken = values[item_idx] * fraction
        total_weight += weight_taken
        
        if fraction == 1.0:
            print(f"  Item {item_idx}: Full item (weight={weights[item_idx]}, "
                  f"value={values[item_idx]:.2f})")
        else:
            print(f"  Item {item_idx}: {fraction:.2%} of item "
                  f"(weight={weight_taken:.2f}/{weights[item_idx]}, "
                  f"value={value_taken:.2f}/{values[item_idx]:.2f})")
    
    print(f"\nTotal weight used: {total_weight:.2f}/{capacity}")
    print("=" * 70)


def main():
    print("FRACTIONAL KNAPSACK PROBLEM - GREEDY METHOD")
    print("=" * 70)
    
    n = int(input("\nEnter number of items: "))
    
    weights = []
    values = []
    
    print("\nEnter weight and value for each item:")
    for i in range(n):
        w = float(input(f"  Item {i} - Weight: "))
        v = float(input(f"  Item {i} - Value: "))
        weights.append(w)
        values.append(v)
    
    capacity = float(input("\nEnter knapsack capacity: "))
    
    max_value, selected_items = fractional_knapsack(weights, values, capacity)
    display_solution(weights, values, capacity, max_value, selected_items)


if __name__ == "__main__":
    main()
