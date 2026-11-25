"""
sorting.py - Parcel Prioritization Module
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Implements Merge Sort to prioritize parcels based on delivery deadline.
Time Complexity: O(n log n) in all cases (best, average, worst).
Space Complexity: O(n) auxiliary space.
Stability: Preserves original arrival order for parcels with identical deadlines.
"""

import csv
import os


def load_parcels(file_path):
    """
    Load parcel records from a CSV file.
    Each parcel contains: parcel_id, destination, weight (kg), value, deadline (hours).
    """
    parcels = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parcels.append({
                "parcel_id": row["parcel_id"].strip(),
                "destination": row["destination"].strip(),
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "deadline": int(row["deadline"])
            })
    return parcels


def merge_sort(items, key="deadline", reverse=False):
    """
    Recursively sorts a list of parcel dictionaries using Divide-and-Conquer Merge Sort.
    """
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], key=key, reverse=reverse)
    right = merge_sort(items[mid:], key=key, reverse=reverse)

    return merge(left, right, key=key, reverse=reverse)


def merge(left, right, key="deadline", reverse=False):
    """
    Combines two sorted sub-lists into a single sorted list.
    Maintains algorithmic stability by using <= for forward sort.
    """
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if not reverse:
            condition = (left[i][key] <= right[j][key])
        else:
            condition = (left[i][key] >= right[j][key])

        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "parcels_small.csv")

    raw_parcels = load_parcels(data_path)
    print(f"Loaded {len(raw_parcels)} parcels from {os.path.basename(data_path)}")
    print("-" * 55)

    sorted_parcels = merge_sort(raw_parcels, key="deadline")

    print(f"{'Parcel ID':<10} {'Destination':<14} {'Weight (kg)':<12} {'Value':<8} {'Deadline (h)':<12}")
    print("-" * 55)
    for p in sorted_parcels:
        print(f"{p['parcel_id']:<10} {p['destination']:<14} {p['weight']:<12} {p['value']:<8} {p['deadline']:<12}")
