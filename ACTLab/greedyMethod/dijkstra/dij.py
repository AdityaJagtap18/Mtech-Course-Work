#!/usr/bin/env python3
"""
Dijkstra's Algorithm - Simple Version
Find shortest path from source to all vertices
"""

import heapq


def dijkstra(vertices, edges, source):
    """
    Dijkstra's algorithm for shortest paths
    
    Args:
        vertices: number of vertices
        edges: list of (u, v, weight) tuples
        source: source vertex
    
    Returns:
        distances: shortest distances from source
    """
    # Build adjacency list
    graph = [[] for _ in range(vertices)]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # Undirected
    
    # Initialize distances
    dist = [float('inf')] * vertices
    dist[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * vertices
    
    print("\nDijkstra's Process:")
    print(f"{'Step':<6} {'Vertex':<10} {'Distance':<12} {'Updated':<30}")
    print("-" * 58)
    
    step = 1
    
    while pq:
        # Get minimum distance vertex
        d, u = heapq.heappop(pq)
        
        if visited[u]:
            continue
        
        visited[u] = True
        updated = []
        
        # Check all neighbors
        for v, weight in graph[u]:
            if not visited[v]:
                new_dist = dist[u] + weight
                
                # Update if shorter
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
                    updated.append(f"V{v}={new_dist}")
        
        updated_str = ", ".join(updated) if updated else "None"
        print(f"{step:<6} V{u:<9} {d:<12} {updated_str:<30}")
        step += 1
    
    print("-" * 58)
    
    return dist


# Main
print("=" * 60)
print("DIJKSTRA'S ALGORITHM - SHORTEST PATH")
print("=" * 60)

# Input
vertices = int(input("\nNumber of vertices: "))
num_edges = int(input("Number of edges: "))

edges = []
print(f"\nEnter {num_edges} edges (vertex1 vertex2 weight):")
for i in range(num_edges):
    u, v, w = map(int, input(f"  Edge {i+1}: ").split())
    edges.append((u, v, w))

source = int(input("\nSource vertex: "))

# Display graph
print("\n" + "-" * 60)
print("Graph Edges:")
for u, v, w in edges:
    print(f"  V{u} -- V{v} (weight={w})")
print("-" * 60)

# Run Dijkstra
distances = dijkstra(vertices, edges, source)

# Display results
print("\n" + "=" * 60)
print("SHORTEST DISTANCES FROM SOURCE")
print("=" * 60)
print(f"Source: V{source}\n")
print(f"{'Vertex':<15} {'Distance':<15}")
print("-" * 30)

for i in range(vertices):
    if distances[i] == float('inf'):
        print(f"V{i:<14} INF (unreachable)")
    else:
        print(f"V{i:<14} {distances[i]}")

print("-" * 30)
print("=" * 60)