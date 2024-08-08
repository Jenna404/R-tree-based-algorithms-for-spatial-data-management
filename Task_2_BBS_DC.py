import time                     # This library is used to measure the time taken for certain operations.
from rtree import index         # This library provides a way to efficiently store and query spatial data.
import heapq                    # Functions for implementing heaps (priority queues), useful for efficiently finding the smallest or largest items.

# Read the dataset from "city2.txt"
def read_dataset():
    homes = []
    with open('city2.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()  # Split the line into parts
            id = parts[0]                 # Extract the home ID
            x = float(parts[1])           # Extract and convert the cost to float
            y = float(parts[2])           # Extract and convert the size to float
            homes.append((id, x, y))      # Append the home data as a tuple to the homes list
    return homes

# Split the dataset into two subspaces based on X dimension (home cost)
def divide_dataset(homes):
    homes.sort(key=lambda home: home[1])  # Sort homes by X dimension (home cost)
    mid = len(homes) // 2
    subspace1 = homes[:mid]  # First half of the homes
    subspace2 = homes[mid:]  # Second half of the homes
    return subspace1, subspace2

# Construct the R-tree to store homes in each subspace for efficient spatial querying:
def construct_rtree(homes):
    p = index.Property()                   # Create an R-tree property object
    rtree_idx = index.Index(properties=p)  # Create an R-tree index with the property object
    for i, (id, x, y) in enumerate(homes):
        rtree_idx.insert(i, (x, y, x, y), obj=(id, x, y))  # Insert with bounding box and object
    return rtree_idx

# Implement the Branch and Bound Skyline (BBS) algorithm to find skyline points in each subspace:
def bbs_algorithm(rtree_idx):
    skyline_bbs = []    # Initialize the list to store skyline points
    heap = []           # Initialize a heap for processing R-tree nodes
    for i in rtree_idx.intersection(rtree_idx.bounds, objects=True):
        heapq.heappush(heap, (i.bbox[0], i.bbox, i.id, i.object))
    
    while heap:
        _, bounds, node_id, home = heapq.heappop(heap)
        if is_skyline_point(home, skyline_bbs):
            skyline_bbs.append(home)  # Add to skyline if it is a skyline point
            for i in rtree_idx.intersection(bounds, objects=True):
                heapq.heappush(heap, (i.bbox[0], i.bbox, i.id, i.object))
    
    return skyline_bbs

# Check if a home is a skyline point
def is_skyline_point(home, skyline_bbs):
    for s in skyline_bbs:
        if dominates(s, home):
            return False
    return True  # If no home in the skyline dominates the current home, return True

# Check if one home dominates another
# A home home1 dominates another home2 if it has a lower cost (x) and a larger or equal size (y).
def dominates(home1, home2):
    return home1[1] <= home2[1] and home1[2] >= home2[2]

# Combine the skylines from two subspaces
def combine_skylines(skyline1, skyline2):
    combined_skyline = []  # Initialize the combined skyline list
    combined_skyline.extend(skyline1)  # Add all points from the first skyline
    for home in skyline2:
        if is_skyline_point(home, combined_skyline):
            combined_skyline.append(home)
    return combined_skyline

# FWrite the output to "Task_2_Output_BBS_DC.txt"
def write_output(filename, skyline_bbs, query_processing_time):
    with open(filename, 'w') as file:
        file.write(f'Query processing time: {query_processing_time:.6f} seconds\n')  # Write query time
        for home in skyline_bbs:
            file.write(f"{home[0]} {home[1]} {home[2]}\n")  # Write each skyline point

# Implement the process and measure query processing time:
def main():
    homes = read_dataset()  # Read the dataset
    subspace1, subspace2 = divide_dataset(homes)  # Divide the dataset into two subspaces
    
    # Construct R-trees for each subspace
    rtree_idx1 = construct_rtree(subspace1)
    rtree_idx2 = construct_rtree(subspace2)
    
    start_time = time.time()  # Start the timer

    # Run the BBS algorithm for each subspace to find skyline points
    skyline1 = bbs_algorithm(rtree_idx1)
    skyline2 = bbs_algorithm(rtree_idx2)
    
    # Combine the skylines from the two subspaces
    combined_skyline = combine_skylines(skyline1, skyline2)
    
    query_start_time = time.time()  # Start the timer for query processing
    query_results = combined_skyline  # The combined skyline results are our final query results
    query_end_time = time.time()
    query_processing_time = query_end_time - query_start_time  # Calculate the query processing time
    
    write_output('Task_2_Output_BBS_DC_v2.txt', query_results, query_processing_time)  # Write the results to the output file

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
