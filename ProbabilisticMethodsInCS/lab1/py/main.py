variations_counter = 1
combination_counter = 1
min_path_len = 10000000
min_path = []

import pandas as pd

data_france = pd.read_csv("france.csv", delimiter=r"\s+", engine="python")


def cycle_length(road):
    length = 0
    for i in range(len(road) - 1):
        city1 = data_france[data_france["Id"] == road[i]]
        city2 = data_france[data_france["Id"] == road[i + 1]]
        
        lat1, lon1 = float(city1.iloc[0]["Latitude"]), float(city1.iloc[0]["Longitude"])
        lat2, lon2 = float(city2.iloc[0]["Latitude"]), float(city2.iloc[0]["Longitude"])
        
        distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
        length += distance
    city1 = data_france[data_france["Id"] == road[0]]
    city2 = data_france[data_france["Id"] == road[len(road) - 1]]
        
    lat1, lon1 = float(city1.iloc[0]["Latitude"]), float(city1.iloc[0]["Longitude"])
    lat2, lon2 = float(city2.iloc[0]["Latitude"]), float(city2.iloc[0]["Longitude"])
    distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    length += distance
    return length


def variations(n, m):
    def backtrack(path, used):
        if len(path) == m:
            global min_path, min_path_len, variations_counter
            if cycle_length(path) < min_path_len:
                min_path_len = cycle_length(path)
                min_path = path.copy() 
            print(variations_counter, ": ", path)
            variations_counter += 1
            return
        for num in range(1, n + 1):
            if num not in used:
                used.add(num)
                path.append(num)
                backtrack(path, used)
                path.pop()
                used.remove(num)

    backtrack([], set())


n, m = 7, 5
variations(n, m)
print("Shortest path: ", min_path_len)

for id in min_path:
    print(data_france.at[id, "Town"], "-> ", end="")
    
print("")

closest_population = 0
cities_closest_population = []

def unique_combinations(n, m, inhabitants_number):
    def backtrack(start, path):
        if len(path) == m:
            global combination_counter, closest_population, cities_closest_population
            print(combination_counter, ": ", *path)
            used = set()
            current_population = 0
            for id in path:
                if id not in used:
                    current_population += data_france.at[id, "Population"]
                used.add(id)
            if abs(current_population - inhabitants_number/2) < abs(closest_population - inhabitants_number/2):
                closest_population = current_population
                cities_closest_population = path
            combination_counter += 1
            return
        numbers = list(range(start, n + 1))
        for num in numbers:
            backtrack(num, path + [num])

    backtrack(1, [])

n, m = 4,5

inhabitants_number = 0

for id in range(0, n):
    inhabitants_number += data_france.at[id, "Population"]

unique_combinations(n, m, inhabitants_number)

print("Closest population: ", closest_population)

used = set()
for id in cities_closest_population:
    if id not in used:
        print(data_france.at[id, "Town"], ", ", end="")
    used.add(id)

    
print("")