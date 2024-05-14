from itertools import permutations
import timeit

# Load the distance matrix from file
def loadDistances():
    with open("citiesAndDistances.txt") as distancesFile:
        cities = distancesFile.readline().split()
        del cities[16:]
        numCities = len(cities)
        
        cityDistances = [[0.0] * numCities for i in range(numCities)]
        
        for i in range(numCities):
            distances = distancesFile.readline().split()
            del distances[0]
            del distances[16:]
            for j in range(len(distances)):
                cityDistances[i][j] = int(distances[j])
    return (cities, cityDistances)

def calculateDistance(route, distances):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i]][route[i + 1]]
    total_distance += distances[route[-1]][route[0]]
    return total_distance

def brute_force(n):
    (cities, distances) = loadDistances()
    routes = permutations(range(n))
    shortest_distance = float('inf')
    best_route = []
    
    for route in routes:
        distance = calculateDistance(route, distances)
        if distance < shortest_distance:
            shortest_distance = distance
            best_route = route

    best_route_cities = [cities[i] for i in best_route] + [cities[best_route[0]]]
    return best_route_cities, shortest_distance

# Test increasing values of n and measure execution time using timeit
for n in range(2, 12):  # Adjust range as needed based on performance
    time_taken = timeit.timeit(lambda: brute_force(n), number=1)
    route, distance = brute_force(n)
    print(f"n = {n}: Shortest route = {route}, Total distance = {distance}, Time = {time_taken:.4f} seconds")
