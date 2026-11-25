"""
main.py - Integrated Mini-Courier Planning System
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Entry point for the Courier Planner application. Seamlessly integrates:
  1. Merge Sort (Divide & Conquer) for parcel urgency sorting
  2. 0/1 Knapsack (Dynamic Programming) for truck capacity optimization
  3. Dijkstra's Algorithm (Greedy Graph Search) for shortest road distances
  4. Nearest-Neighbor TSP (Heuristic Search) for closed-loop delivery routing
"""

import os
import sys

from sorting import load_parcels, merge_sort
from knapsack import knapsack_01
from dijkstra import load_graph, dijkstra, reconstruct_path
from tsp import nearest_neighbor_tsp


def run_courier_planner(use_large=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if use_large:
        parcels_file = os.path.join(base_dir, "..", "data", "parcels_large.csv")
        graph_file = os.path.join(base_dir, "..", "data", "graph_large.json")
        capacity = 50
        dataset_name = "LARGE DATASET (Scalability Prototype)"
    else:
        parcels_file = os.path.join(base_dir, "..", "data", "parcels_small.csv")
        graph_file = os.path.join(base_dir, "..", "data", "graph_small.json")
        capacity = 20
        dataset_name = "SMALL DATASET (Baseline Prototype)"

    print("=" * 65)
    print(f"MINI-COURIER PLANNER - {dataset_name}")
    print("=" * 65)

    # 1. Load Data
    raw_parcels = load_parcels(parcels_file)
    network = load_graph(graph_file)
    print(f"Total Parcels Ingested : {len(raw_parcels)}")
    print(f"Road Network Vertices  : {len(network)} locations")
    print(f"Truck Cargo Capacity   : {capacity} kg")

    # Step 1: Sorting
    print("\n" + "-" * 65)
    print("[1] PARCEL PRIORITIZATION (Merge Sort by Deadline)")
    print("-" * 65)
    sorted_parcels = merge_sort(raw_parcels, key="deadline")
    sample_preview = sorted_parcels[:min(6, len(sorted_parcels))]
    for p in sample_preview:
        print(f"  * {p['parcel_id']:<6} -> Dest: {p['destination']:<5} | Weight: {p['weight']:>2} kg | "
              f"Value: {p['value']:>2} | Deadline: {p['deadline']:>2}h")
    if len(sorted_parcels) > 6:
        print(f"    ... and {len(sorted_parcels) - 6} more parcels sorted.")

    # Step 2: Knapsack Packing
    print("\n" + "-" * 65)
    print("[2] VEHICLE BOX FILLING (0/1 Knapsack Dynamic Programming)")
    print("-" * 65)
    max_value, chosen_parcels, _ = knapsack_01(sorted_parcels, capacity)
    packed_weight = sum(p["weight"] for p in chosen_parcels)
    print(f"  * Parcels Selected       : {len(chosen_parcels)}")
    id_list = [p['parcel_id'] for p in chosen_parcels]
    if len(id_list) > 16:
        id_str = ", ".join(id_list[:16]) + ",\n                           " + ", ".join(id_list[16:])
    else:
        id_str = ", ".join(id_list)
    print(f"  * Selected Parcel IDs    : [{id_str}]")
    print(f"  * Total Weight Loaded    : {packed_weight} kg / {capacity} kg ({packed_weight / capacity * 100:.1f}%)")
    print(f"  * Total Utility/Value    : {max_value} points")

    # Step 3: Shortest Paths via Dijkstra
    stops = sorted({p["destination"] for p in chosen_parcels})
    print("\n" + "-" * 65)
    print("[3] DELIVERY DESTINATIONS & GRAPH ROUTING (Dijkstra's Algorithm)")
    print("-" * 65)
    if len(stops) > 12:
        stops_str = ", ".join(repr(s) for s in stops[:12]) + ",\n                             " + ", ".join(repr(s) for s in stops[12:])
    else:
        stops_str = ", ".join(repr(s) for s in stops)
    print(f"  * Delivery Stops to Visit: [{stops_str}] ({len(stops)} unique locations)")

    all_stops = ["Depot"] + stops
    dist_matrix = {}
    prev_matrix = {}
    for loc in all_stops:
        dist_matrix[loc], prev_matrix[loc] = dijkstra(network, loc)

    # Step 4: TSP Route
    print("\n" + "-" * 65)
    print("[4] DELIVERY TOUR OPTIMIZATION (Nearest-Neighbor TSP)")
    print("-" * 65)
    tour, total_km = nearest_neighbor_tsp("Depot", stops, dist_matrix)
    print("  * Ordered Visiting Tour:")
    print("    " + " -> ".join(tour))
    print(f"\n  * Total Driving Distance : {total_km} km")

    print("\nSegment-by-Segment Waypoint Manifest:")
    for u, v in zip(tour, tour[1:]):
        path_nodes = reconstruct_path(prev_matrix[u], v)
        path_str = " -> ".join(path_nodes)
        print(f"    {u:<6} -> {v:<6} : {dist_matrix[u][v]:>2} km   (Shortest Path: {path_str})")

    print("=" * 65)
    print(f"FINAL PLAN SUMMARY: {len(chosen_parcels)} parcels | {len(stops)} stops | {total_km} km total")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    is_large = (len(sys.argv) > 1 and sys.argv[1].lower() in ["large", "--large", "-l"])
    run_courier_planner(use_large=is_large)
