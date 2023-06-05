import csv
import itertools
import matplotlib.pyplot as plt

def calculate_distance(point1, point2):
    x1, y1, _ = point1
    x2, y2, _ = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def tsp(points):
    # Find the magazine point
    magazine = next((point for point in points if point[2] == "Magazine"), None)
    if magazine is None:
        raise ValueError("Magazine point not found.")

    # Remove the magazine from the points list temporarily
    points_without_magazine = [point for point in points if point[2] != "Magazine"]

    # Generate all possible permutations of the points without the magazine
    permutations = itertools.permutations(points_without_magazine)

    # Initialize variables
    shortest_distance = float('inf')
    shortest_path = None

    # Iterate through all permutations
    for path in permutations:
        path_with_magazine = [magazine] + list(path)

        total_distance = 0

        # Calculate the total distance of the current path
        for i in range(len(path_with_magazine) - 1):
            total_distance += calculate_distance(path_with_magazine[i], path_with_magazine[i+1])

        # Update the shortest distance and path if the current path is shorter
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path_with_magazine

    return shortest_distance, shortest_path

def read_points_from_csv(filename):
    points = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            point_id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            points.append((x, y, point_id))
    return points

def get_path_ids(path):
    return [point[2] for point in path]

def draw_path(points, path_ids):
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, 'o', label='Points')
    plt.plot(x_coords[-1], y_coords[-1], 'go', label='Ending Point')

    # Draw the path using IDs
    for i in range(len(path_ids) - 1):
        start_id = path_ids[i]
        end_id = path_ids[i+1]

        start_point = next(point for point in points if point[2] == start_id)
        end_point = next(point for point in points if point[2] == end_id)

        plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], 'b-')

    # Add labels near the points
    for point in points:
        if point[2] == "Magazine":
            plt.plot(point[0], point[1], 'ro', label='Starting Point')
        else:
            plt.plot(point[0], point[1], 'ro')
        plt.annotate(str(point[2]), (point[0], point[1]), textcoords="offset points", xytext=(0, 10), ha='center')

    # Display the shortest path on top of the graph
    shortest_path = " -> ".join(str(point_id) for point_id in path_ids)
    plt.text(0.5, 1.1, f"Shortest Path: {shortest_path}", transform=plt.gca().transAxes, ha='center')

    plt.title('TSP Path')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()

# Usage
filename = 'points.csv'  # Replace with your CSV filename
points = read_points_from_csv(filename)

# Add the starting point (magazine) as the first point
starting_point = (50,50, "Magazine")
points.insert(0, starting_point)

distance, path = tsp(points)

path_ids = get_path_ids(path)

print("Shortest distance:", distance)
print("Shortest path (IDs):", path_ids)

draw_path(points, path_ids)