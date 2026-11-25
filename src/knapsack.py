"""
knapsack.py - Vehicle Box Filling & Packing Optimization
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Implements 0/1 Knapsack Dynamic Programming to select the subset of prioritized
parcels that maximizes total value/utility without exceeding vehicle weight capacity.
Time Complexity: O(n * W), where n is the number of parcels and W is vehicle capacity.
Space Complexity: O(n * W) for the 2D DP table enabling full backtracking.
"""

import os
from sorting import load_parcels, merge_sort


def knapsack_01(parcels, capacity):
    """
    Solves 0/1 Knapsack using bottom-up Dynamic Programming.

    Parameters:
        parcels: List of dicts, each with 'weight' and 'value'.
        capacity: Maximum integer capacity (kg) of the delivery truck.

    Returns:
        (max_value, selected_parcels, dp_table)
    """
    n = len(parcels)
    # dp[i][w] stores maximum value achievable using a subset of first i parcels with weight limit w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item_w = parcels[i - 1]["weight"]
        item_v = parcels[i - 1]["value"]
        for w in range(capacity + 1):
            if item_w > w:
                # Cannot include parcel i-1 because it exceeds current capacity w
                dp[i][w] = dp[i - 1][w]
            else:
                # Maximize between excluding and including parcel i-1
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - item_w] + item_v)

    # Backtracking to reconstruct the exact subset of chosen parcels
    selected = []
    rem_w = capacity
    for i in range(n, 0, -1):
        if dp[i][rem_w] != dp[i - 1][rem_w]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            rem_w -= parcel["weight"]

    selected.reverse()
    return dp[n][capacity], selected, dp


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "parcels_small.csv")
    CAPACITY = 20

    raw = load_parcels(data_path)
    prioritized = merge_sort(raw, key="deadline")

    max_val, chosen, table = knapsack_01(prioritized, CAPACITY)

    print("=" * 60)
    print(f"0/1 KNAPSACK DYNAMIC PROGRAMMING TABLE (Capacity 0..{CAPACITY} kg)")
    print("=" * 60)
    header = "Item  | " + " ".join(f"{c:2}" for c in range(CAPACITY + 1))
    print(header)
    print("-" * len(header))

    for idx, row in enumerate(table):
        label = "none" if idx == 0 else prioritized[idx - 1]["parcel_id"]
        print(f"{label:<5} | " + " ".join(f"{val:2}" for val in row))

    total_wt = sum(p["weight"] for p in chosen)
    print("\n" + "=" * 60)
    print("OPTIMAL DISPATCH PACKING RESULT:")
    print("=" * 60)
    print(f"Total Value Achieved : {max_val} points")
    print(f"Vehicle Utilization  : {total_wt} kg / {CAPACITY} kg ({total_wt / CAPACITY * 100:.1f}%)")
    print(f"Selected Parcel IDs  : {[p['parcel_id'] for p in chosen]}")
    print("\nSelected Parcel Breakdown:")
    for p in chosen:
        print(f"  * {p['parcel_id']}: Destination={p['destination']}, Weight={p['weight']} kg, "
              f"Value={p['value']}, Deadline={p['deadline']}h")
