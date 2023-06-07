import csv
import itertools
import matplotlib.pyplot as plt
import time
import random

start_time = time.time()


def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def tsp(points):
    points_without_magazine = [point for point in points[1:]]  # Ignorowanie pierwszego elementu (Magazine)
    num_points = len(points_without_magazine)
    distance_cache = {}

    # Inicjalizacja losowego rozwiązania
    current_path = [points[0]] + random.sample(points_without_magazine, num_points)
    current_distance = 0

    # Obliczanie początkowej odległości
    for i in range(num_points):
        current_distance += calculate_distance(current_path[i], current_path[i+1])

    # Hill Climbing - przeszukiwanie lokalne
    while True:
        best_distance = current_distance
        best_path = current_path

        # Generowanie sąsiadów
        for i in range(1, num_points):
            for j in range(i + 1, num_points + 1):
                new_path = current_path[:i] + list(reversed(current_path[i:j])) + current_path[j:]

                # Obliczanie odległości dla nowego rozwiązania
                new_distance = current_distance - calculate_distance(current_path[i-1], current_path[i]) \
                               - calculate_distance(current_path[j-1], current_path[j]) \
                               + calculate_distance(new_path[i-1], new_path[i]) \
                               + calculate_distance(new_path[j-1], new_path[j])

                # Aktualizacja najlepszego rozwiązania
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_path = new_path

        # Sprawdzenie warunku zakończenia
        if best_distance == current_distance:
            break

        # Aktualizacja bieżącego rozwiązania
        current_distance = best_distance
        current_path = best_path

    return best_distance, best_path

def generate_csv_file(row_count):
    with open('points.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'x', 'y', 'demand'])

        for i in range(row_count):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            z = random.randint(100, 200)
            writer.writerow([i+1, x, y, z])


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

    # Draw the path using IDs
    for i in range(len(path_ids) - 1):
        start_id = path_ids[i]
        end_id = path_ids[i + 1]

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

    # Plot the ending point
    ending_point = next(point for point in points if point[2] == path_ids[-1])
    plt.plot(ending_point[0], ending_point[1], 'go', label='Ending Point')

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
generate_csv_file(23)
filename = 'points.csv'  # Replace with your CSV filename
points = read_points_from_csv(filename)

# Add the starting point (magazine) as the first point
starting_point = (50,50, "Magazine")
points.insert(0, starting_point)

distance, path = tsp(points)

path_ids = get_path_ids(path)

print("Shortest distance:", distance)
print("Shortest path (IDs):", path_ids)
print("Execution time: %s seconds ---" % (round(time.time() - start_time,2)))

draw_path(points, path_ids)