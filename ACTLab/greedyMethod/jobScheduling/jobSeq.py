#!/usr/bin/env python3
"""
Job Scheduling with Deadlines - Greedy Method

Algorithm:
1. Sort jobs by profit in descending order (Greedy choice - pick highest profit first)
2. For each job, find the latest available time slot before its deadline
3. Schedule the job in that slot if available
"""

class Job:
    """Class to represent a job with id, deadline, and profit"""
    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit
    
    def __repr__(self):
        return f"Job{self.job_id}(deadline={self.deadline}, profit={self.profit})"


def job_scheduling(jobs):
    """
    Schedule jobs to maximize profit using greedy method
    
    Args:
        jobs: list of Job objects
    
    Returns:
        scheduled_jobs: list of scheduled jobs with time slots
        total_profit: maximum profit achieved
    """
    n = len(jobs)
    
    # Sort jobs by profit in descending order (Greedy choice)
    jobs.sort(key=lambda x: x.profit, reverse=True)
    
    # Find maximum deadline to determine number of time slots
    max_deadline = max(job.deadline for job in jobs)
    
    # Initialize time slots (all empty initially)
    time_slots = [-1] * max_deadline  # -1 means slot is free
    scheduled_jobs = []
    total_profit = 0
    
    print("\nGreedy Job Scheduling Process:")
    print("=" * 80)
    print(f"{'Job ID':<10} {'Deadline':<12} {'Profit':<12} {'Scheduled At':<20} {'Status':<15}")
    print("-" * 80)
    
    # Try to schedule each job
    for job in jobs:
        # Find a free slot for this job (start from deadline and go backwards)
        for slot in range(min(max_deadline, job.deadline) - 1, -1, -1):
            if time_slots[slot] == -1:  # Slot is free
                # Schedule this job
                time_slots[slot] = job.job_id
                scheduled_jobs.append((job, slot + 1))  # slot+1 for 1-indexed time
                total_profit += job.profit
                print(f"{job.job_id:<10} {job.deadline:<12} {job.profit:<12} "
                      f"Slot {slot + 1:<16} {'SCHEDULED':<15}")
                break
        else:
            # No free slot found
            print(f"{job.job_id:<10} {job.deadline:<12} {job.profit:<12} "
                  f"{'N/A':<20} {'REJECTED':<15}")
    
    print("-" * 80)
    
    return scheduled_jobs, total_profit, time_slots


def display_solution(scheduled_jobs, total_profit, time_slots):
    """Display the final solution"""
    print("\n" + "=" * 80)
    print("JOB SCHEDULING SOLUTION")
    print("=" * 80)
    
    print(f"\nTotal Profit: {total_profit}")
    print(f"Number of Jobs Scheduled: {len(scheduled_jobs)}")
    
    print("\nScheduled Jobs (in time order):")
    scheduled_jobs.sort(key=lambda x: x[1])  # Sort by time slot
    
    for job, slot in scheduled_jobs:
        print(f"  Time Slot {slot}: Job {job.job_id} (profit={job.profit}, deadline={job.deadline})")
    
    print("\nTime Slot Allocation:")
    print("  ", end="")
    for i, job_id in enumerate(time_slots):
        if job_id == -1:
            print(f"Slot {i+1}: Empty  ", end="")
        else:
            print(f"Slot {i+1}: Job{job_id}  ", end="")
        if (i + 1) % 4 == 0:
            print("\n  ", end="")
    print("\n" + "=" * 80)


def main():
    print("JOB SCHEDULING WITH DEADLINES - GREEDY METHOD")
    print("=" * 80)
    
    n = int(input("\nEnter number of jobs: "))
    
    jobs = []
    
    print("\nEnter deadline and profit for each job:")
    for i in range(n):
        deadline = int(input(f"  Job {i+1} - Deadline: "))
        profit = int(input(f"  Job {i+1} - Profit: "))
        jobs.append(Job(i + 1, deadline, profit))
    
    print(f"\nInput Jobs:")
    for job in jobs:
        print(f"  {job}")
    
    scheduled_jobs, total_profit, time_slots = job_scheduling(jobs)
    display_solution(scheduled_jobs, total_profit, time_slots)


if __name__ == "__main__":
    main()