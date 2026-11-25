"""
benchmark.py - Scalability and Runtime Benchmarking Module
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Benchmarks the execution time (in milliseconds) and verifies the correctness
of each core algorithmic step across increasing parcel input sizes (25, 50, 100, 200).
"""

import os
import time

from sorting import load_parcels, merge_sort
from knapsack import knapsack_01
from dijkstra import load_graph, dijkstra
from tsp import nearest_neighbor_tsp

REPEATS = 20
CAPACITY = 50
SIZES = [25, 50, 100, 200]


def benchmark_function(func, *args):
    """
    Measures the average execution time of func(*args) over REPEATS iterations.
    Returns: (average_ms, function_result)
    """
    start_time = time.perf_counter()
    for _ in range(REPEATS):
        result = func(*args)
    avg_ms = ((time.perf_counter() - start_time) / REPEATS) * 1000.0
    return avg_ms, result


def run_all_benchmarks():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parcels_file = os.path.join(base_dir, "..", "data", "parcels_large.csv")
    graph_file = os.path.join(base_dir, "..", "data", "graph_large.json")

    all_parcels = load_parcels(parcels_file)
    network = load_graph(graph_file)

    benchmark_records = []

    for n in SIZES:
        subset = all_parcels[:n]

        # 1. Benchmark Merge Sort
        t_sort, sorted_sub = benchmark_function(merge_sort, subset, "deadline")
        is_sorted_valid = [p["deadline"] for p in sorted_sub] == sorted(p["deadline"] for p in subset)

        # 2. Benchmark 0/1 Knapsack
        t_knapsack, (best_val, chosen, _) = benchmark_function(knapsack_01, sorted_sub, CAPACITY)
        unique_stops = sorted({p["destination"] for p in chosen})

        # 3. Benchmark Dijkstra from Depot
        t_dijkstra, _ = benchmark_function(dijkstra, network, "Depot")

        # 4. Benchmark Full Route Planning (All-Pairs Dijkstra for stops + Nearest Neighbor TSP)
        def plan_tour():
            locs = ["Depot"] + unique_stops
            dist_mat = {loc: dijkstra(network, loc)[0] for loc in locs}
            return nearest_neighbor_tsp("Depot", unique_stops, dist_mat)

        t_route, (tour, route_km) = benchmark_function(plan_tour)

        benchmark_records.append({
            "n": n,
            "t_sort": t_sort,
            "t_knapsack": t_knapsack,
            "t_dijkstra": t_dijkstra,
            "t_route": t_route,
            "sorted_ok": is_sorted_valid,
            "selected_count": len(chosen),
            "packed_weight": sum(p["weight"] for p in chosen),
            "total_value": best_val,
            "stops_count": len(unique_stops),
            "route_km": route_km
        })

    return benchmark_records


if __name__ == "__main__":
    records = run_all_benchmarks()

    print("=" * 65)
    print(f"EMPIRICAL RUNTIME ANALYSIS (Milliseconds, averaged over {REPEATS} runs)")
    print("=" * 65)
    print(f"{'Parcels (N)':>12} {'Merge Sort':>12} {'0/1 Knapsack':>14} {'Dijkstra (1x)':>14} {'Route Tour':>12}")
    print("-" * 65)
    for r in records:
        print(f"{r['n']:>12} {r['t_sort']:>11.3f}ms {r['t_knapsack']:>12.3f}ms "
              f"{r['t_dijkstra']:>12.3f}ms {r['t_route']:>10.3f}ms")

    print("\n" + "=" * 65)
    print("CORRECTNESS AND OPTIMIZATION VERIFICATION")
    print("=" * 65)
    print(f"{'Parcels':>8} {'Sorted?':>10} {'Selected':>10} {'Weight':>8} {'Value':>8} {'Stops':>8} {'Route km':>10}")
    print("-" * 65)
    for r in records:
        print(f"{r['n']:>8} {str(r['sorted_ok']):>10} {r['selected_count']:>10} "
              f"{r['packed_weight']:>6}kg {r['total_value']:>8} {r['stops_count']:>8} {r['route_km']:>8} km")
    print("=" * 65)
