###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Eric Nielsen
# Collaborators: N/A
# Time: 3:00PM

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = dict() # initialize an empty dictionary
    try:
        with open(file=filename, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                name, weight = line.strip().split(",")
                cows[name] = int(weight)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' could not be found")
    except IOError as e:
        # Catches other I/O related errors (e.g., permission issues)
        print(f"I/O error: {e}")
    return cows

cows = load_cows("./assignments/first assignment/ps1_cow_data.txt")

def pretty_print_cows(cows):
    for i, (name, weight) in enumerate(cows.items()):
        print(f"[{i + 1}] {name.title()}: {weight}")

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips

    """
    
    trips = []
    remaining = sorted(cows, key=cows.get, reverse=True)

    while remaining:
        trip, trip_weight = [], 0
        leftover = []
        for name in remaining:
            weight = cows[name]
            if trip_weight + weight <= limit:
                trip.append(name)
                trip_weight += weight 
            else:
                leftover.append(name)
        trips.append(trip)
        remaining = leftover
    return trips

trips = greedy_cow_transport(cows)

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    def calc_trip_weight(trip, cows):
        weight_sum = 0
        for name in trip:
            weight = cows[name]
            weight_sum += weight 
            
        return weight_sum

    ps = get_partitions(cows) # generate the power set 
    trip_dict = dict()
    success_partitions = dict()
    for cow_part in ps:
        valid_part = True
        for trip in cow_part:
            str_trip = str(trip)
            trip_weight = trip_dict.get(str_trip)
            if trip_weight is None:
                trip_weight = calc_trip_weight(trip, cows)
                trip_dict[str_trip] = trip_weight
            
            if trip_weight > limit: # no point in searching anymore
                valid_part = False
                break
        
        if valid_part:
            success_partitions[str(cow_part)] = len(cow_part)
    
    shortest_trip = success_partitions[min(success_partitions, key=success_partitions.get)]
    return shortest_trip

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    def test_func_speed(label, func, cows, limit=10):
        print(f"\n=== TESTING {label} ===\n")
        start = time.perf_counter()
        output = func(cows, limit)
        end = time.perf_counter()
        elapsed = end - start
        print(f"OUTPUT: {output}\nEXECUTION TIME (ms): {elapsed}")
    
    labels = ["Greedy Algorithm", "Brute Force Algorithm"]
    funcs = [greedy_cow_transport, brute_force_cow_transport]

    for i, func in enumerate(funcs):
        test_func_speed(labels[i], func, cows, limit=20)


compare_cow_transport_algorithms()