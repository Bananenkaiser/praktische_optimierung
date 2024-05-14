"""Der Handlungsreisende fragt Dich, ob die die Rundreiselängen und Rechenzeiten von
2-opt verbessern kannst. Du entscheidest Dich Simulated Annealing (SA) eine Chance zu
geben.
1. Implementiere den SA Algorithmus.

2. Der Perturbationsoperator (OP) soll als ein Kombinationsoperator implementiert
werden, der bei jedem Aufruf zufällig eine der folgenden Operationen durchführt
• ein Schritt des Algorithmus node exchange,
• ein Schritt des Algoirthmus node insertion oder
• ein Schritt des Algorithmus two_opt_xchg(tour, i, k).

3. Stelle einige Experimente mit verschiedenen Abkühlschemas und deren Parametern
an und wähle die beste Kombination.

4. Lasse SA fünf Mal laufen und berichte die Rundreiselängen, die durchschnittliche
Anzahl der Berechnungen einer Rundreiselänge und die durchschnittliche Rechenzeit. Trage die Werte in die Tabelle ein.

5. Für bekannte kürzeste Rundreisen: Findet SA auch immer die kürzeste Rundreise?
Wenn nicht, wie nahe kommt SA an eine beste Lösung?

6. Nimmt die Rechenzeit von SA mit größer werdenden n zu?

7. Ist Deine SA Implementierung schneller als 2-opt?

8. Erzeugt Dein SA bessere Lösungen als 2-opt?
"""


import math
import random
import timeit

def loadDistances(n=None):
    with open("citiesAndDistances.txt") as distancesFile:
        cities = distancesFile.readline().strip().split()
        if n is not None:
            cities = cities[:n]
        numCities = len(cities)
        
        cityDistances = [[0.0] * numCities for _ in range(numCities)]
        
        for i in range(numCities):
            distances = distancesFile.readline().strip().split()
            cityDistances[i] = list(map(int, distances[1:1+numCities]))
            
    return cities, cityDistances

def two_opt_xchg(tour, i, k):
    if i >= k or i < 0 or k >= len(tour):
        raise ValueError("Invalid indices: i must be less than k and both must be within the range of the tour length.")
    new_tour = tour[:]
    new_tour[i:k+1] = reversed(tour[i:k+1])
    return new_tour

def measurePath(tour, distances, city_index):
    length = 0
    for i in range(len(tour) - 1):
        length += distances[city_index[tour[i]]][city_index[tour[i + 1]]]
    length += distances[city_index[tour[-1]]][city_index[tour[0]]]  # Complete the cycle
    return length

def two_opt_step(tour, distances, city_index):
    num_evaluations = 0
    shortest_length = measurePath(tour, distances, city_index)
    shortest_tour = tour[:]
    length_changed = True
    
    while length_changed:
        length_changed = False
        for i in range(1, len(tour) - 1):
            for k in range(i + 1, len(tour)):
                new_tour = two_opt_xchg(tour, i, k)
                new_distance = measurePath(new_tour, distances, city_index)
                num_evaluations += 1
                if new_distance < shortest_length:
                    shortest_tour = new_tour[:]
                    shortest_length = new_distance
                    length_changed = True
        if length_changed:
            tour = shortest_tour[:]
    
    return shortest_tour, shortest_length, num_evaluations

def initialize_random_tour(cities):
    tour = cities[:]
    random.shuffle(tour)
    return tour

def hill_climber(cities, distances):
    city_index = {cities[i]: i for i in range(len(cities))}
    current_tour = initialize_random_tour(cities)
    num_total_evaluations = 0
    improvement = True

    start_time = timeit.default_timer()

    while improvement:
        improved_tour, improved_length, evaluations = two_opt_step(current_tour, distances, city_index)
        if improved_length < measurePath(current_tour, distances, city_index):
            current_tour = improved_tour[:]
            num_total_evaluations += evaluations
        else:
            improvement = False

    elapsed_time = timeit.default_timer() - start_time

    return current_tour, measurePath(current_tour, distances, city_index), num_total_evaluations, elapsed_time


def node_exchange(tour):
    i, j = sorted(random.sample(range(len(tour)), 2))
    tour[i], tour[j] = tour[j], tour[i]
    return tour

def node_insertion(tour):
    i, j = sorted(random.sample(range(len(tour)), 2))
    node = tour.pop(i)
    tour.insert(j, node)
    return tour

def perturbation_operator(tour):
    tour_copy = tour[:]
    operation = random.choice([0, 1, 2])  # Choose operation type
    if operation == 0:
        return node_exchange(tour_copy)
    elif operation == 1:
        return node_insertion(tour_copy)
    elif operation == 2:
        i, k = sorted(random.sample(range(1, len(tour) - 1), 2))
        return two_opt_xchg(tour_copy, i, k)

def loadDistances(n=None):
    with open("citiesAndDistances.txt") as distancesFile:
        cities = distancesFile.readline().strip().split()
        if n is not None:
            cities = cities[:n]
        numCities = len(cities)

        cityDistances = [[0.0] * numCities for _ in range(numCities)]

        for i in range(numCities):
            distances = distancesFile.readline().strip().split()
            cityDistances[i] = list(map(int, distances[1:1+numCities]))

    return cities, cityDistances

def simulated_annealing(cities, distances, initial_temp=1000, cooling_rate=0.95, num_iterations=100):
    city_index = {city: i for i, city in enumerate(cities)}
    current_tour = random.sample(cities, len(cities))
    current_length = measurePath(current_tour, distances, city_index)
    T = initial_temp
    evaluations = 0

    while T > 1:
        for _ in range(num_iterations):
            new_tour = perturbation_operator(current_tour[:])
            new_length = measurePath(new_tour, distances, city_index)
            evaluations += 1
            if new_length < current_length or math.exp((current_length - new_length) / T) > random.random():
                current_tour = new_tour
                current_length = new_length
        T *= cooling_rate
    
    return current_length, evaluations, T

num_trials = 5
city_sizes = range(5, 17)  # From 5 to 16 cities
results = {n: {'lengths': [], 'evaluations': [], 'times': []} for n in city_sizes}

for trial in range(1, num_trials + 1):
    print(f"Trial {trial}")
    for n in city_sizes:
        cities, cityDistances = loadDistances(n)
        start_time = timeit.default_timer()
        length, evaluations, _ = simulated_annealing(cities, cityDistances)
        elapsed_time = timeit.default_timer() - start_time
        results[n]['lengths'].append(length)
        results[n]['evaluations'].append(evaluations)
        results[n]['times'].append(elapsed_time)
        print(f"n = {n}: Length = {length}")

# Averaging results
print("\nAverage results across trials:")
for n in city_sizes:
    avg_evaluations = sum(results[n]['evaluations']) / num_trials
    avg_time = sum(results[n]['times']) / num_trials
    lengths = results[n]['lengths']
    print(f"n = {n}: Average Evaluations = {avg_evaluations}, Average Time = {avg_time:.6f} seconds, Lengths = {lengths}")