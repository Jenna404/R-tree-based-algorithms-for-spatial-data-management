# The BBS algorithm is a direct method to find skyline points using the R-tree data structure.

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

# Construct the R-tree from the homes dataset:
def construct_rtree(homes):
    p = index.Property()                   # Create an R-tree property object
    rtree_idx = index.Index(properties=p)  # Create an R-tree index with the property object
    for i, (id, x, y) in enumerate(homes):
        rtree_idx.insert(i, (x, y, x, y), obj=(id, x, y))  # Insert home into the R-tree with the bounding box and home detail as an object
    return rtree_idx

# Implement the Branch and Bound Skyline (BBS) algorithm to find skyline points using the R-tree index:
def bbs_algorithm(rtree_idx):
    skyline_bbs = []       # Initialize the list to store skyline points
    heap = []              # Initialize a heap for processing R-tree nodes
    # The R-tree is queried to find initial entries, which are pushed onto the heap.
    # The heap is processed until it’s empty.
    for i in rtree_idx.intersection(rtree_idx.bounds, objects=True):
        heapq.heappush(heap, (i.bbox[0], i.bbox, i.id, i.object))
    
    while heap:
        _, bounds, node_id, home = heapq.heappop(heap)
        if is_skyline_point(home, skyline_bbs):
            skyline_bbs.append(home)        # Add to skyline if the home is a skyline point
            for i in rtree_idx.intersection(bounds, objects=True):
                heapq.heappush(heap, (i.bbox[0], i.bbox, i.id, i.object))  # Entries within the current node's bounds are pushed back onto the heap for further processing.
    
    return skyline_bbs

# Check if a home is a skyline point
def is_skyline_point(home, skyline_bbs):
    for s in skyline_bbs:
        if dominates(s, home):
            return False    # If any point in the skyline dominates the given home (checked using dominates), it returns False.
    return True  # If no home in the skyline dominates the current home, return True

# Check if one home dominates another:
# A home home1 dominates another home2 if it has a lower cost (x) and a larger or equal size (y).
def dominates(home1, home2):
    return home1[1] <= home2[1] and home1[2] >= home2[2]

# Write the output to "Task_2_Output_BBS.txt"
def write_output(filename, skyline_bbs, query_processing_time):
    with open(filename, 'w') as file:
        file.write(f'Query processing time: {query_processing_time:.6f} seconds\n')  # Write query time
        for home in skyline_bbs:
            file.write(f"{home[0]} {home[1]} {home[2]}\n")  # Write each skyline point

# Implement the process and measure query processing time:
def main():
    homes = read_dataset()  # Read the dataset
    rtree_idx = construct_rtree(homes)  # Construct the R-tree
    
    # Run the BBS algorithm to find skyline points
    skyline_bbs = bbs_algorithm(rtree_idx)

    # Measure the time taken to process the query
    query_start_time = time.time()
    query_results = skyline_bbs  # Assuming BBS results are the final query results for skyline points
    query_end_time = time.time()
    query_processing_time = query_end_time - query_start_time

    # Write the results to the output file
    write_output('Task_2_Output_BBS.txt', query_results, query_processing_time)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
