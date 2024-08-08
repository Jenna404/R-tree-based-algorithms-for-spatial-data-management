import time
from rtree import index as rtree_index
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Load dataset from file function
def load_data(file_path):
    points = []
    with open(file_path, 'r') as dataset:
        for index, line in enumerate(dataset):
            if index >= 200: 
                break
            data = line.strip().split()
            point = (int(data[0]), float(data[1]), float(data[2]))
            points.append(point)
            print(f"id={point[0]}, x={point[1]:.2f}, y={point[2]:.2f}")
    return points


#Sequential_scan_algorythm

# Euclidean distance function
def euclidean_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

radius = 10.0  # Define a specific radius

def process_queries(points, query_points, radius=10.0):
    results = []
    start_time = time.time()
    for query in query_points:
        query_id, query_x, query_y = query 
        count = 0
        for point in points:
            if euclidean_distance(point[1], point[2], query_x, query_y) <= radius:
                count += 1
        results.append((query_id, count))
    end_time = time.time()
    total_time = end_time - start_time
    average_time_per_query = total_time / len(query_points) if query_points else 0
    return results, total_time, average_time_per_query


points = load_data("restaurant_dataset.txt")  # Load facility points
query_points = load_data("query_points.txt")  # Load query points

# Process queries
results, total_time, average_time_per_query = process_queries(points, query_points)

# Output results
output_path = "sequential_scan_results.txt"
with open(output_path, 'w') as output_file:
    # Write header for clarity
    output_file.write("Query ID, Count of Points Within Distance\n")
    # Convert each tuple to a string and write to file
    for result in results:
        output_file.write(f"Query ID {result[0]}: {result[1]} points found\n")
    # Write processing time information
    output_file.write(f"\nTotal processing time: {total_time:.4f} seconds\n")
    output_file.write(f"Average time per query: {average_time_per_query:.4f} seconds\n")

print("Results have been written to", output_path)


#Best_First_(BF)_algorythm
# Function to create an R-tree index from dataset
def create_index(points):
    # Define the properties of the R-tree index
    prop = rtree_index.Property()
    prop.leaf_capacity = 100  # Can be adjusted for optimal performance
    prop.index_capacity = 100  # Can be adjusted for optimal performance
    prop.near_minimum_overlap_factor = 40  # Must be less than the leaf and index capacity
    prop.overwrite = True
    
    # Create the R-tree index with the specified properties
    idx = rtree_index.Index(properties=prop)
    for point in points:
        # Each point is inserted into the index with its coordinates forming a bounding box
        idx.insert(point[0], (point[1], point[2], point[1], point[2]), obj=point)
    return idx

# Function to find the nearest restaurant using the Best First Algorithm
def query_index(idx, query):
    query_id, query_x, query_y = query
    nearest = list(idx.nearest((query_x, query_y, query_x, query_y), 1, objects='raw'))[0]
    return (query_id, nearest[0], nearest[1], nearest[2])

def best_first_search(idx, query_points):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(query_index, idx, query) for query in query_points]
        results = [future.result() for future in futures]
    total_time = time.time() - start_time
    average_time = total_time / len(query_points)
    return results, total_time, average_time

# Load points and queries
points = load_data("restaurant_dataset.txt")
query_points = load_data("query_points.txt")

# Create R-tree index from restaurant data
index = create_index(points)

# Measure start time before initiating Best First Search
start_time = time.time()

# Process queries using Best First Search
bf_results, bf_total_time, bf_average_time_per_query = best_first_search(index, query_points)

# Output results for Best First Algorithm
output_path_bf = "best_first_results.txt"
with open(output_path_bf, 'w') as output_file:
    output_file.write("Query ID, Nearest Point ID, X, Y\n")
    for result in bf_results:
        output_file.write(f"Query ID {result[0]}: Nearest Point ID {result[1]} at ({result[2]:.2f}, {result[3]:.2f})\n")
    output_file.write(f"\nTotal processing time: {bf_total_time:.4f} seconds\n")
    output_file.write(f"Average time per query: {bf_average_time_per_query:.4f} seconds\n")

print("Best First Search results have been written to", output_path_bf)

#Divide_and_Conquer_Algorythm

def split_data_by_median(points, coordinate='x'):
    coord_index = 1 if coordinate == 'x' else 2
    points_sorted = sorted(points, key=lambda x: x[coord_index])
    median_index = len(points_sorted) // 2
    return points_sorted[:median_index], points_sorted[median_index:]

def best_first_search_divide_conquer(trees, query_points):
    results = []
    start_time = time.time()
    for query in query_points:
        query_id, query_x, query_y = query
        best_point = None
        min_distance = float('inf')
        for tree in trees:
            nearest = list(tree.nearest((query_x, query_y, query_x, query_y), 1, objects='raw'))[0]
            distance = euclidean_distance(query_x, query_y, nearest[1], nearest[2])
            if distance < min_distance:
                min_distance = distance
                best_point = nearest
        results.append((query_id, best_point[0], best_point[1], best_point[2], min_distance))
    end_time = time.time()
    total_time = end_time - start_time
    average_time = total_time / len(query_points)
    return results, total_time, average_time

def create_index(points):
    idx = rtree_index.Index()  
    for point in points:
        idx.insert(point[0], (point[1], point[2], point[1], point[2]), obj=point)
    return idx

subspace1, subspace2 = split_data_by_median(points)
tree1 = create_index(subspace1)
tree2 = create_index(subspace2)

# Process queries using Divide-and-Conquer Best First Search
results, total_time, average_time = best_first_search_divide_conquer([tree1, tree2], query_points)

# Output results for divide and conquer method
output_path = "divide_conquer_best_first_results.txt"
with open(output_path, 'w') as output_file:
    output_file.write("Query ID, Nearest Point ID, X, Y, Distance\n")
    for result in results:
        output_file.write(f"Query ID {result[0]}: Nearest Point ID {result[1]} at ({result[2]:.2f}, {result[3]:.2f}) Distance: {result[4]:.2f}\n")
    output_file.write(f"\nTotal processing time: {total_time:.4f} seconds\n")
    output_file.write(f"Average time per query: {average_time:.4f} seconds\n")