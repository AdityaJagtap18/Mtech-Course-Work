#!/usr/bin/env python3
"""
Activity Selection Problem - Greedy Method

Algorithm:
1. Sort activities by finish time (earliest finish first)
2. Select first activity
3. For remaining activities, select if start time >= last finish time
"""


def activity_selection(start, finish):
    """
    Select maximum activities using greedy method
    
    Args:
        start: list of start times
        finish: list of finish times
    
    Returns:
        selected: list of selected activity indices
    """
    n = len(start)
    
    # Create list of activities with (start, finish, index)
    activities = []
    for i in range(n):
        activities.append((start[i], finish[i], i))
    
    # Sort by finish time (Greedy choice - pick activity that finishes earliest)
    activities.sort(key=lambda x: x[1])
    
    print("\n" + "=" * 80)
    print("ACTIVITY SELECTION PROCESS")
    print("=" * 80)
    print("\nSorted by finish time:")
    print(f"{'Activity':<12} {'Start':<12} {'Finish':<12}")
    print("-" * 36)
    for start_time, finish_time, idx in activities:
        print(f"A{idx+1:<11} {start_time:<12} {finish_time:<12}")
    print("-" * 36)
    
    # Select activities
    selected = []
    last_finish_time = -1
    
    print("\n" + "=" * 80)
    print("GREEDY SELECTION:")
    print("=" * 80)
    print(f"{'Activity':<12} {'Start':<12} {'Finish':<12} {'Status':<20} {'Reason':<30}")
    print("-" * 80)
    
    for start_time, finish_time, idx in activities:
        if start_time >= last_finish_time:
            # Can select this activity
            selected.append(idx)
            reason = "First activity" if last_finish_time == -1 else f"Start({start_time}) >= Last finish({last_finish_time})"
            print(f"A{idx+1:<11} {start_time:<12} {finish_time:<12} {'SELECTED':<20} {reason:<30}")
            last_finish_time = finish_time
        else:
            # Overlaps with last selected activity
            reason = f"Start({start_time}) < Last finish({last_finish_time})"
            print(f"A{idx+1:<11} {start_time:<12} {finish_time:<12} {'REJECTED':<20} {reason:<30}")
    
    print("-" * 80)
    
    return selected


def main():
    print("=" * 80)
    print("ACTIVITY SELECTION PROBLEM - GREEDY METHOD")
    print("=" * 80)
    
    # Get input
    n = int(input("\nEnter number of activities: "))
    
    start = []
    finish = []
    
    print("\nEnter start and finish time for each activity:")
    for i in range(n):
        s = int(input(f"  Activity {i+1} - Start time: "))
        f = int(input(f"  Activity {i+1} - Finish time: "))
        start.append(s)
        finish.append(f)
    
    # Display input
    print("\n" + "-" * 80)
    print("INPUT ACTIVITIES:")
    print("-" * 80)
    print(f"{'Activity':<12} {'Start Time':<15} {'Finish Time':<15}")
    print("-" * 80)
    for i in range(n):
        print(f"A{i+1:<11} {start[i]:<15} {finish[i]:<15}")
    print("-" * 80)
    
    # Perform activity selection
    selected = activity_selection(start, finish)
    
    # Display results
    print("\n" + "=" * 80)
    print("FINAL SOLUTION")
    print("=" * 80)
    print(f"\nMaximum number of activities: {len(selected)}")
    print(f"\nSelected activities:")
    
    # Sort selected activities by original index for display
    selected_sorted = sorted(selected)
    for idx in selected_sorted:
        print(f"  Activity A{idx+1}: Start={start[idx]}, Finish={finish[idx]}")
    
    print(f"\nActivity sequence: {' → '.join([f'A{i+1}' for i in selected_sorted])}")
    

    
    print("\n" + "=" * 80)
    print(f"✓ Total activities performed: {len(selected)} out of {n}")
    print(f"✓ Activities rejected: {n - len(selected)}")
    print("=" * 80)


if __name__ == "__main__":
    main()