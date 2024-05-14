"""Da der Handlungsreisende alle Landeshauptstädte besuchen möchte, fragt er Dich, ob
Du für n = 16 eine Rundreise berechnen könntest. Die Rundreise muss nicht optimal sein,
aber doch so kurz wie möglich. Der Handlungsreisende wäre mit einer Antwort, die in
einigen Minuten berechenbar ist, zufrieden.
Schreibe eine 2-opt Heuristik. Teile Deine Implementierung in drei Funktionen auf.

1. Implementiere die Funktion two_opt_xchg(tour, I, k), die die Reihenfolge der
Städte i; :::; k in tour umdreht und die neue Rundreise zurückgibt.

2. Implementiere danach die Funktion two_opt_step(tour), die die best-improvement
Strategie realisiert. Dafür muss two_opt_step alle sinnvollen 2-opt Vertauschungen
von tour durchführen und die kürzeste neue Rundreise sich merken sowie zurückgeben.
Es sollte beachtet werden, dass ein 2-opt Tausch (two_opt_xchg) bei der
best-improvement Strategie immer auf die original-tour angewendet wird. Zähle
auch die Anzahl der ausgewerteten Rundreiselängen und lasse auch diese Größe
zurückgeben.

3. Implementiere einen Hill Climber, der, ausgehend von einer zufälligen Startlösung,
two_opt_step(tour) solange aufruft, solange eine Verbesserung der Rundreise möglich
ist. Kann die Rundreise nicht mehr verbessert werden, lasse die Länge der
Rundreise, die Anzahl berechneter Rundreiselängen und die Rechenzeit ausgeben.

4. Berechne für n = 5; :::; 16 die Rundreisen mit 2-opt.

5. Da 2-opt ein nichtdeterministischer (randomisierter) Algorithmus ist, lasse ihn fünf
Mal laufen und berichte die Rundreiselängen, die durchschnittliche Anzahl der Berechnungen
einer Rundreiselänge und die durchschnittliche Rechenzeit. Trage die
Werte in die Tabelle ein.

6. Für bekannte kürzeste Rundreisen: Findet 2-opt auch immer die kürzeste Rundreise?
Wenn nicht, wie nahe kommt 2-opt an eine beste Lösung?

7. Nimmt die 2-opt Rechenzeit mit größer werdenden n zu?"""

import timeit
import random

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

def measurePath(p, distances, city_index):
    length = 0
    for i in range(len(p)):
        length += distances[city_index[p[i-1]]][city_index[p[i]]]
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

cities, cityDistances = loadDistances()
city_index = {cities[i]: i for i in range(len(cities))}

# Timing the two_opt_step function
start_time = timeit.default_timer()
shortest_tour, shortest_length, num_evaluations = two_opt_step(list(cities), cityDistances, city_index)
elapsed_time = timeit.default_timer() - start_time

print(f"Modifizierte Tour: {shortest_tour}")
print(f"Kürzeste Rundreiselänge: {shortest_length}")
print(f"Anzahl berechneter Rundreiselängen: {num_evaluations}")
print(f"Rechenzeit: {elapsed_time} Sekunden")
print()


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


final_tour, final_length, total_evaluations, total_time = hill_climber(cities, cityDistances)

print(f"Endgültige Tour: {final_tour}")
print(f"Kürzeste Rundreiselänge: {final_length}")
print(f"Anzahl berechneter Rundreiselängen: {total_evaluations}")
print(f"Rechenzeit: {total_time} Sekunden")
print()

results = []

for n in range(5, 17):  # From 5 to 16 cities
    cities, cityDistances = loadDistances(n)
    city_index = {cities[i]: i for i in range(len(cities))}
    current_tour = initialize_random_tour(cities)  # Random starting tour

    start_time = timeit.default_timer()
    shortest_tour, shortest_length, num_evaluations = two_opt_step(current_tour, cityDistances, city_index)
    elapsed_time = timeit.default_timer() - start_time
    
    results.append({
        "n": n,
        "tour": shortest_tour,
        "length": shortest_length,
        "evaluations": num_evaluations,
        "time": elapsed_time
    })

# Output the results
for result in results:
    print(f"n = {result['n']}: Length = {result['length']}, Evaluations = {result['evaluations']}, Time = {result['time']:.6f} seconds,  Tour = {result['tour']}")


# Define the range of cities to be tested (from 5 to 16)
city_sizes = range(5, 17)

# Initialize lists to hold cumulative results for evaluations and time
cumulative_evaluations = {n: 0 for n in city_sizes}
cumulative_time = {n: 0 for n in city_sizes}
cumulative_lengths = {n: [] for n in city_sizes}

# Number of trials to average results over
num_trials = 5

# Running the loop for each size of cities
for trial in range(num_trials):
    print(f"Trial {trial + 1}")
    for n in city_sizes:
        cities, cityDistances = loadDistances(n)
        city_index = {cities[i]: i for i in range(len(cities))}
        current_tour = initialize_random_tour(cities)  # Random starting tour

        start_time = timeit.default_timer()
        shortest_tour, shortest_length, num_evaluations = two_opt_step(current_tour, cityDistances, city_index)
        elapsed_time = timeit.default_timer() - start_time

        # Accumulate results for averaging
        cumulative_evaluations[n] += num_evaluations
        cumulative_time[n] += elapsed_time
        cumulative_lengths[n].append(shortest_length)

        print(f"n = {n}: Length = {shortest_length}")

# Output average results for evaluations and time
print("\nAverage results across trials:")
for n in city_sizes:
    avg_evaluations = cumulative_evaluations[n] / num_trials
    avg_time = cumulative_time[n] / num_trials
    print(f"n = {n}: Average Evaluations = {avg_evaluations}, Average Time = {avg_time:.6f} seconds, Lengths = {cumulative_lengths[n]}")
