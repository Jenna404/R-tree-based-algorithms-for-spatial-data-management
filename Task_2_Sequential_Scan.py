import time             #This library is used to measure the time taken for certain operations.

# Load data from file into a list of dictionaries
points = []
with open('city2.txt', 'r') as dataset:
    for line in dataset.readlines():  # Read each line in the file
        data = line.split()  # Split the line into parts
        points.append(
            {
                'id': int(data[0]),    # Parse and store ID
                'x': float(data[1]),   # Parse and store x-coordinate (cost)
                'y': float(data[2])    # Parse and store y-coordinate (size)
            }
        )

def is_dominated(p1, p2):
    """
    Check if point p1 is dominated by point p2.
    Args:
        p1 (dict): The first point with keys 'id', 'x', 'y'.
        p2 (dict): The second point with keys 'id', 'x', 'y'.
    Returns:
        bool: True if p2 dominates p1, False otherwise.
    """
    return p2['x'] <= p1['x'] and p2['y'] >= p1['y']  # p2 is cheaper and larger than p1

def skyline_sequential(points):
    """
    Find the skyline using the Sequential Scan Based Method.
    Args:
        points (list of dicts): The list of points.
    Returns:
        list of dicts: The skyline points.
    """
    skyline = []  # Initialize the list to store skyline points
    for p1 in points:  # Iterate through each point
        dominated = False
        for p2 in points:  # Compare with every other point
            if p1 != p2 and is_dominated(p1, p2):  # If p1 is dominated by p2
                dominated = True
                break  # No need to check further if p1 is dominated
        if not dominated:  # If p1 is not dominated by any other point
            skyline.append(p1)  # Add p1 to the skyline
    return skyline

def write_output(filename, skyline, query_time):
    """
    Write the output to a text file.
    Args:
        filename (str): The name of the output file.
        skyline (list of dicts): The skyline points.
        query_time (float): The time taken to process the query.
    """
    with open(filename, 'w') as file:
        file.write(f'Query processing time: {query_time:.6f} seconds\n')  # Write query time
        for point in skyline:
            file.write(f"{point['id']} {point['x']} {point['y']}\n")  # Write each skyline point

def query_points(points, query):
    """
    Query the points within the given range.
    Args:
        points (list of dicts): The list of points.
        query (dict): The query range with keys 'x1', 'x2', 'y1', 'y2'.
    Returns:
        list of dicts: The points that fall within the query range.
    """
    result = []
    for point in points:
        if query['x1'] <= point['x'] <= query['x2'] and query['y1'] <= point['y'] <= query['y2']:
            result.append(point)
    return result

def main():
    # Define queries
    queries = [
        {
            'x1': 17840,
            'x2': 18840,
            'y1': 13971,
            'y2': 14971
        }
    ]
    
    print("The current query is", queries)
    
    # Find skyline using Sequential Scan Based Method
    skyline = skyline_sequential(points)  # Compute the skyline points
    
    # Measure the time taken to process the queries
    results = []
    query_start_time = time.time()
    for query in queries:
        results.extend(query_points(skyline, query))
    query_end_time = time.time()
    query_processing_time = query_end_time - query_start_time
    
    print(f"There are {len(results)} data points included in the query.")
    print(f"The query processing time is {query_processing_time:.6f} seconds.")
    
    # Write the output to a file
    write_output('Task_2_Output_Sequential.txt', skyline, query_processing_time)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
