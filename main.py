import itertools
import csv
import matplotlib.pyplot as plt

def calculate_distance(point1, point2):
    x1, y1, _, _ = point1
    x2, y2, _, _ = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def tsp(points, num_vehicles, vehicle_capacity):
    # Find the magazine point
    magazine = next((point for point in points if point[3] == "Magazine"), None)
    if magazine is None:
        raise ValueError("Magazine point not found.")

    # Remove the magazine from the points list temporarily
    points_without_magazine = [point for point in points if point[3] != "Magazine"]

    # Generate all possible permutations of the points without the magazine
    permutations = itertools.permutations(points_without_magazine)

    # Initialize variables
    shortest_distance = float('inf')
    shortest_paths = None

    # Iterate through all permutations
    for path in permutations:
        path_with_magazine = [magazine] + list(path)
        current_capacity = vehicle_capacity
        current_distance = 0
        current_paths = [[] for _ in range(num_vehicles)]

        for point in path_with_magazine:
            if point[2] == "Magazine":
                current_capacity = vehicle_capacity
                current_paths[0].append(point)
            else:
                if point[2] > current_capacity:
                    current_capacity = vehicle_capacity
                    current_paths[num_vehicles - 1].append(magazine)
                    current_paths[num_vehicles - 1].append(point)
                else:
                    current_capacity -= point[2]
                    current_paths[num_vehicles - 1].append(point)

        for i in range(num_vehicles):
            for j in range(len(current_paths[i]) - 1):
                current_distance += calculate_distance(current_paths[i][j], current_paths[i][j+1])

        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_paths = current_paths

    return shortest_distance, shortest_paths


def read_points_from_csv(filename):
    points = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            point_id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            capacity = row[3]
            points.append((x, y, point_id, capacity))
    return points

def draw_paths(points, paths):
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    plt.figure(figsize=(8, 6))

    # Plot points
    plt.plot(x_coords, y_coords, 'o', label='Points')
    plt.plot(x_coords[-1], y_coords[-1], 'go', label='Ending Point')

    # Plot paths for each vehicle
    for i, path in enumerate(paths):
        color = 'b' if i % 2 == 0 else 'g'  # Alternate between blue and green colors

        # Get starting point for the path
        start_point = next(point for point in points if point[2] == "Magazine")

        # Plot path using IDs
        for j in range(len(path) - 1):
            start_id = path[j][2]
            end_id = path[j+1][2]

            start_point = next(point for point in points if point[2] == start_id)
            end_point = next(point for point in points if point[2] == end_id)

            plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color + '-')

        # Display remaining capacity for the vehicle
        vehicle_capacity = points[start_id][3]
        plt.annotate(f"Vehicle {i+1} Capacity: {vehicle_capacity}", (start_point[0], start_point[1]),
                     textcoords="offset points", xytext=(0, -20), ha='center')

    # Add labels near the points
    for point in points:
        if point[2] == "Magazine":
            plt.plot(point[0], point[1], 'ro', label='Starting Point')
        else:
            plt.plot(point[0], point[1], 'ro')
        plt.annotate(str(point[2]), (point[0], point[1]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title('TSP Paths')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()

# Usage
filename = 'points.csv'  # Replace with your CSV filename
points = read_points_from_csv(filename)

# Add the starting point (magazine) as the first point
starting_point = (50, 50, "Magazine", 0)
points.insert(0, starting_point)

num_vehicles = 3
vehicle_capacity = 1000

distance, paths = tsp(points, num_vehicles, vehicle_capacity)

print("Shortest distance:", distance)
for i, path in enumerate(paths):
    print(f"Vehicle {i+1} path (IDs):", [point[2] for point in path])

draw_paths(points, paths)
