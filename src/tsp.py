"""
tsp.py - Route Optimization & Delivery Tour Planning
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Implements the Nearest-Neighbor Heuristic for the Traveling Salesperson Problem (TSP)
to determine the courier's visiting sequence across customer delivery points.
Time Complexity: O(k^2) where k is the number of delivery stops, combined with
Dijkstra's all-pairs shortest paths across the required stops: O(k * (V + E) log V).
"""

import os
from sorting import load_parcels, merge_sort
from knapsack import knapsack_01
from dijkstra import load_graph, dijkstra, reconstruct_path


def nearest_neighbor_tsp(depot, delivery_stops, dist_matrix):
    """
    Constructs a closed delivery tour starting and ending at depot.
    Greedily advances to the closest unvisited destination at each step.

    Parameters:
        depot: Name of the origin depot vertex.
        delivery_stops: Iterable of customer delivery destinations.
        dist_matrix: Dict of dicts containing shortest road distance between any two locations.

    Returns:
        (tour, total_distance)
    """
    unvisited = set(delivery_stops)
    tour = [depot]
    current = depot
    total_distance = 0

    while unvisited:
        # Pick the nearest unvisited customer stop
        next_stop = min(sorted(unvisited), key=lambda s: dist_matrix[current][s])
        leg_dist = dist_matrix[current][next_stop]
        total_distance += leg_dist
        tour.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    # Return to the depot to complete the cycle
    return_dist = dist_matrix[current][depot]
    total_distance += return_dist
    tour.append(depot)

    return tour, total_distance


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parcels_path = os.path.join(base_dir, "..", "data", "parcels_small.csv")
    graph_path = os.path.join(base_dir, "..", "data", "graph_small.json")
    CAPACITY = 20

    raw = load_parcels(parcels_path)
    sorted_p = merge_sort(raw, key="deadline")
    _, selected, _ = knapsack_01(sorted_p, CAPACITY)

    # Unique delivery locations
    stops = sorted({p["destination"] for p in selected})
    road_graph = load_graph(graph_path)

    # Compute all-pairs shortest distances between Depot and delivery locations
    all_locations = ["Depot"] + stops
    dist_map = {}
    prev_map = {}

    for loc in all_locations:
        dist_map[loc], prev_map[loc] = dijkstra(road_graph, loc)

    route, route_len = nearest_neighbor_tsp("Depot", stops, dist_map)

    print("=" * 60)
    print("ROUTE OPTIMIZATION RESULT (Nearest-Neighbor TSP)")
    print("=" * 60)
    print("Selected Parcels :", [p["parcel_id"] for p in selected])
    print("Delivery Stops   :", stops)
    print(f"Tour Sequence    : {' -> '.join(route)}")
    print(f"Total Tour Length: {route_len} km\n")

    print("Segment-by-Segment Navigation:")
    print("-" * 60)
    for u, v in zip(route, route[1:]):
        subpath = " -> ".join(reconstruct_path(prev_map[u], v))
        print(f"  {u:<5} -> {v:<5} : {dist_map[u][v]:>2} km   (Via road: {subpath})")
    print("-" * 60)
    print(f"ROUND-TRIP TOTAL: {route_len} km")
