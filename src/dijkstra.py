"""
dijkstra.py - Shortest Path Computation Module
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Implements Dijkstra's Single-Source Shortest Path Algorithm with a min-heap priority queue.
Time Complexity: O((V + E) log V), where V is the number of locations and E is the number of roads.
Space Complexity: O(V) for distances and predecessor map.
"""

import heapq
import json
import os


def load_graph(file_path):
    """
    Load the road network graph from a JSON file.
    Format: { "NodeA": { "NodeB": distance_km, ... }, ... }
    """
    with open(file_path, mode="r", encoding="utf-8") as f:
        return json.load(f)


def dijkstra(graph, source):
    """
    Computes shortest distance from source to all other reachable nodes.

    Returns:
        dist: Dict mapping node -> minimum distance from source
        prev: Dict mapping node -> predecessor node on the shortest path
    """
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}

    dist[source] = 0
    # Priority queue stores tuples of (distance_so_far, node)
    pq = [(0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        # Skip outdated entries in the heap
        if curr_dist > dist[u]:
            continue

        for v, weight in graph[u].items():
            if curr_dist + weight < dist[v]:
                dist[v] = curr_dist + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, destination):
    """
    Rebuilds the sequence of nodes along the shortest path using the predecessor dictionary.
    """
    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()
    return path


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(base_dir, "..", "data", "graph_small.json")

    network = load_graph(graph_path)
    src_node = "Depot"

    distances, predecessors = dijkstra(network, src_node)

    print("=" * 60)
    print(f"DIJKSTRA'S SHORTEST PATHS FROM {src_node}")
    print("=" * 60)
    print(f"{'Destination':<15} {'Distance (km)':<15} {'Full Path Trajectory'}")
    print("-" * 60)

    for node in sorted(network.keys()):
        if node == src_node:
            continue
        d = distances[node]
        full_path = " -> ".join(reconstruct_path(predecessors, node))
        print(f"{node:<15} {d:<15} {full_path}")
