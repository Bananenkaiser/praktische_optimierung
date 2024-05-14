from itertools import permutations
from random import shuffle

# load the distnace matrix from file
def loadDistances():
	distancesFile = open("citiesAndDistances.txt")
	cities = distancesFile.readline().split()
	del cities[16:]
	numCities = len(cities)
	
	# create an empty 2-dimensional matrix
	cityDistances = [[0.0] * numCities for i in range(numCities)]
	
	# for all cities:
	for i in range(numCities):
		distances = distancesFile.readline().split()
		del distances[0]
		del distances[16:]
		for j in range(len(distances)):
			cityDistances[i][j] = int(distances[j])
	return (cities,cityDistances)


def measurePath(p, distances):
	length = 0
	for i in range(len(p)):
		length += distances[p[i-1]][p[i]]
	return length


# example implementation of the random walk algorithm
# consider only cities from 0 to maximalNoOfCities
def random_walk(maximalNoOfCities):
	
	# get the longest trip length for an upper bound
	# sum up all distances of a 2-dimensional list
	shortestTourLength = sum([sum(i) for i in distances])
	
	# for one million steps do: randomly sample a tour and compute the 
	# length. if better tour found, remember it
	for j in range(1000000):
		
		# sample random permutation
		p=list(range(maximalNoOfCities))
		shuffle(p)
		
		# measure path length
		tourLength = measurePath(p, distances)
		
		# if new path is shorter than the old best path, remember the new path
		if tourLength < shortestTourLength:
			shortestTourLength = tourLength
			shortestTour = p
			
			#print the new shortest path
			shortestTourCities = [cities[i] for i in shortestTour]
			print("iteration: {} tour: {} length: {}".format(j,shortestTourCities, shortestTourLength))
		
			# do some status printing from time to time
		elif j % 100000 == 0:
			print('iteration: {}'.format(j))	
	
# try first with 16 cities
maximalNoOfCities=16

# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
print(cities[:maximalNoOfCities])

# print distance matrix
print(distances)

# do random walk search for 1000000 steps
random_walk(maximalNoOfCities)



