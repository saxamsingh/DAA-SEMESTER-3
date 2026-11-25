"""
generate_data.py - Synthetic Large Dataset Generator
Course: Design & Analysis of Algorithms (ETCCDA302)
Student: Saksham Singh | Roll No: 2501730270

Generates a connected 31-node road network and a 200-parcel dataset
for empirical scalability and runtime performance testing.
"""

import csv
import json
import os
import random

# Seed with Saksham's university roll number for deterministic, reproducible results
random.seed(2501730270)

NUM_LOCATIONS = 30
NUM_PARCELS = 200

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# 1. Generate Road Network
nodes = ["Depot"] + [f"N{i}" for i in range(1, NUM_LOCATIONS + 1)]
network = {node: {} for node in nodes}


def add_road(u, v, dist):
    network[u][v] = dist
    network[v][u] = dist


# Connect sequential chain to guarantee global reachability
for i in range(1, len(nodes)):
    add_road(nodes[i - 1], nodes[i], random.randint(2, 9))

# Add cross-connecting arterial roads (shortcuts)
for _ in range(NUM_LOCATIONS * 2):
    u, v = random.sample(nodes, 2)
    if v not in network[u]:
        add_road(u, v, random.randint(3, 15))

graph_file = os.path.join(data_dir, "graph_large.json")
with open(graph_file, "w", encoding="utf-8") as f:
    json.dump(network, f, indent=2)

# 2. Generate Parcels
parcels_file = os.path.join(data_dir, "parcels_large.csv")
with open(parcels_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["parcel_id", "destination", "weight", "value", "deadline"])
    for i in range(1, NUM_PARCELS + 1):
        writer.writerow([
            f"P{i}",
            f"N{random.randint(1, NUM_LOCATIONS)}",
            random.randint(1, 10),      # weight in kg
            random.randint(1, 10),      # value / priority score
            random.randint(1, 72)       # delivery deadline in hours
        ])

print("Synthetic Dataset Generation Complete:")
print(f"  * Created {graph_file} ({len(nodes)} locations, undirected connected graph)")
print(f"  * Created {parcels_file} ({NUM_PARCELS} parcel records)")
