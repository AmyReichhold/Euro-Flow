"""
Author: Amy Reichhold

Euro-Flow
"""
import csv

# Global cost dictionary.
country_day_cost = {}
country_cost = {}
transportation_cost = {}

# Global origin cities.
origin_cities = []

# Global valid countries to visit in Europe.
countries = []

CHECK_VALIDATOR = False


def sequence_cost(sequence):
    if len(sequence) > 1:
        cost = 0
        for i in range(len(sequence) - 1):
            cost += transportation_cost[(sequence[i], sequence[i + 1])]
        return cost
    else:
        return 0

def validator(origin, locations):
    # try all possibilities for flying from the origin to one of the other
    # locations, and then visiting all the other locations from that location,
    # and returning back to that location.

    if not locations:
        return [origin]
    else:
        min_cost_circuit = None
        min_cost = float('inf')
        for location in locations:
            # create a list not including location, so that we can tally the
            # cost of using that location to start our European circuit
            remaining_locations = list(locations)
            remaining_locations.remove(location)

            # get the min cost sequence for visiting the remaining locations
            sequence = validator_helper(location, remaining_locations, location)

            # get the total cost of starting at the origin, visiting this
            # location, visiting the remaining locations (for minimum cost),
            # and returning to this location

            trip = [origin] + sequence + [location]
            cost = sequence_cost(trip)

            # if this cost is less expensive than the minimum cost so far,
            # then update
            if cost < min_cost:
                min_cost_circuit = trip
                min_cost = cost

        return min_cost_circuit

def validator_helper(origin, locations, endpoint):
    if not locations:
        return [origin, endpoint]
    else:
        min_cost_sequence = None
        min_cost = float('inf')
        for location in locations:
            new_locations = list(locations)
            new_locations.remove(location)
            sequence = [origin]
            sequence += validator_helper(location, new_locations, endpoint)
            cost = sequence_cost(sequence)
            if cost < min_cost:
                min_cost_sequence = sequence
                min_cost = cost
        return min_cost_sequence


def MST_Prim(G, w, r):
    """
    G = (vertices, edges)
    w = edge weights
    r = root vertex
    """
    V = G[0]
    E = G[1]
    
    key = dict()
    parent = dict()

    # Go through all the vertices in G.
    for u in V:
        key[u] = float('inf')
        parent[u] = None

    key[r] = 0

    # Min-priority queue Q.
    Q = list(V)

    while Q:
        u = Extract_Min(Q, key)
        for v in get_neighbors_in_queue(Q, u, E):
            if v in Q and w[u, v] < key[v]:
                parent[v] = u
                key[v] = w[u, v]

    # A is the edges in the minimum spanning tree.
    A = []
    
    for v in V:
        if v == r:
            pass
        else:
            A.append((v, parent[v]))

    return A


def get_neighbors_in_queue(Q, u, E):
    neighbors = []
    for edge in E:
        if u == edge[0]:
            neighbors.append(edge[1])
        else:
            continue

    queue_neighbors = []
    for v in Q:
        if v in neighbors:
            queue_neighbors.append(v)
        else:
            continue
    
    return queue_neighbors


def Extract_Min(Q, key):
    min_val = float('inf')
    min_vertex = None
    if Q:
        min_val = key[Q[0]]
        min_vertex = Q[0]
        for v in Q:
            if key[v] < min_val:
                min_vertex = v
                min_val = key[v]
        
        # Remove minimum vertex from the min-priority queue.
        if min_vertex:
            Q.remove(min_vertex)

    return min_vertex


def get_children(r, A):
    children = []
    # Loop through the edges in A.
    for edge in A:
        # Check if current node is the parent.
        if r == edge[1]:
            children.append(edge[0])
    return children


def pre_order(r, A):
    result = [r]
    # Get current nodes children.
    children = get_children(r, A)

    # Traverse tree in Pre-Order: Node, Left, Right.
    for child in children:
        result += pre_order(child, A)

    return result


def main():
    #TODO

    # Open the origin cities file that contains all the cities you can fly from.
    with open('origin_cities.csv', 'r') as f:
        origin_cities_file = csv.reader(f)
        next(origin_cities_file)
        
        for city in origin_cities_file:
            origin_cities.append(city[0])

    print('You can fly from:')
    for city in origin_cities:
        #print(f'You can fly from: \n{origin_cities[city]}: {city}')
        print(f'{city} ',end=" ")
    print()
    print()

    # Get the origin city the user want's to fly from.
    VALID_ORIGIN = False
    while not VALID_ORIGIN:
        origin_input = input('Please type the city you want to fly from: ')
        origin = origin_input.lower()
        if origin.capitalize() in origin_cities:
            VALID_ORIGIN = True
        else:
            print(f'{origin_input} is not valid.\n')
    print()


    # Open the countries file that contains all the countries the user can visit.
    with open('countries.txt', 'r') as f:
        header = next(f)

        countries_file = f.readlines()
        
        for country in countries_file:
            countries.append(str(country).strip())
    
    print('You can travel to:')
    for country in countries:
        print(f'{country} ', end=" ")
    print()
    print()

    # Get the countries the user want's to visit.
    VALID_LOCATIONS = False
    while not VALID_LOCATIONS:
        countries_input = input('Please type the space-separated countries you want to travel to: ').lower()
        locations = countries_input.split(' ')
        print()

        total_valid = 0
        for location in locations:
            if location.capitalize() in countries:
                total_valid += 1
            else:
                print(f'{location} is not a valid country.\n')
        if total_valid == len(locations):
            VALID_LOCATIONS = True
    
    # Get the user's budget from the command line.
    budget = int(input('What is your budget? '))
    print()
    print()
    print()

    # Get the graph vertices.
    V = locations
    V.append(origin)

    for location in locations:
        transportation_cost[(location, location)] = 0

    E = []

    # Open and read in the transportation file.
    with open('transportation.csv', 'r') as f:
        transportation_data = csv.reader(f)
        header = next(transportation_data)
        #print(f'header: {header}')

        # Populating transportation_cost dictionary and getting the
        # graphs edges.
        for row in transportation_data:
            #print(f'row: {row}')
            if row[0] == origin:
                transportation_cost[(row[0], row[1])] = float(row[2])
            else:
                if row[0] in locations:
                    transportation_cost[(row[0], row[1])] = float(row[2])
        E = list(transportation_cost.keys())

    # Creating touple G, which is a Graph with vertices V and edges E.
    G = (V, E)

    # Calling Prim's algorithm which creates a Minimum Spanning Tree A.
    A = MST_Prim(G, transportation_cost, origin)

    # Calling Pre-Order function on A, starting at the origin.
    path_v = pre_order(origin, A)

    # The flight from the origin is a round trip, so appending the first 
    # country visited from the origin to the end of the path because we 
    # want to return back there to fly back to the origin.
    path_v.append(path_v[1])
    path_v.append(path_v[0])

    # Creating the path edges from the vertices returned from Pre-Order.
    path = []
    for i in range(len(path_v) - 2):
        path.append((path_v[i], path_v[i+1]))

    # Calculating the transportation costs of the path.
    total_cost = 0
    for edge in path:
        total_cost += transportation_cost[edge]

    if CHECK_VALIDATOR:
        # Calling the validator function that exhaustively checks every path
        # to ensure that the minimum path was found.
        print('Calling validator function...')
        locations.remove(origin)
        validator_path = validator(origin, locations)
        print(f'validator_path: {validator_path}')

        val_cost = sequence_cost(validator_path)
        print(f'total_cost: {total_cost}, val_cost: {val_cost}')

    # Open and read in the country every day cost file.
    with open('sample_data.csv', 'r') as f:
        country_data = csv.reader(f)
        header = next(country_data)

        for row in country_data:
            country = row[0]
            day_costs = []
            total_day_cost = 0
            for cost in row:
                if cost != country:
                    day_costs.append(float(cost))
                    total_day_cost += float(cost)
                    total_cost += float(cost)
            country_day_cost[country] = day_costs
            country_cost[country] = total_day_cost

    if total_cost > budget:
        print(f'I\'m sorry, the cost of the trip is ${total_cost:.2f}, which is out of your budget.')
        print()
    else:
        print(f'Congratulations! You can afford this trip!')
        print(f'The minimum cost is ${total_cost:.2f}.')
        print()

    # Write the itinerary to an output file.
    with open('Itinerary.txt', 'w') as f:
        f.write('Euro-Flow Itinerary\n\n')
        for edge in path:
            if edge[0] == origin:
                f.write(f'You are flying from {edge[0].capitalize()}'
                        f' to {edge[1].capitalize()} for' 
                        f' ${transportation_cost[(edge[0], edge[1])]:.2f} round trip.\n')
                f.write(f'\tA day in {edge[1].capitalize()} costs'
                        f' ${country_cost[edge[1]]:.2f}.\n')
                f.write(f'\t\tFood costs ${country_day_cost[edge[1]][0]:.2f}.\n')
                f.write(f'\t\tLodging costs ${country_day_cost[edge[1]][2]:.2f}.\n')
                f.write(f'\t\tLocal Transportation costs ${country_day_cost[edge[1]][1]:.2f}.\n\n')
            else:
                f.write(f'You are traveling from {edge[0].capitalize()} to'
                        f' {edge[1].capitalize()} by train for'
                        f' ${transportation_cost[(edge[0], edge[1])]:.2f}.\n')
                f.write(f'\tA day in {edge[1].capitalize()} costs'
                        f' ${country_cost[edge[1]]:.2f}.\n')
                f.write(f'\t\tFood costs ${country_day_cost[edge[1]][0]:.2f}.\n')
                f.write(f'\t\tLodging costs ${country_day_cost[edge[1]][2]:.2f}.\n')
                f.write(f'\t\tLocal Transportation costs ${country_day_cost[edge[1]][1]:.2f}.\n\n')
        f.write(f'The total cost for transportation and 1 night stays for each\n'
                f' country is ${total_cost:.2f}.\n')


    print(f'The itinerary for the cheapest trip is found in the \'Itinerary.txt\' file.')


    return 0


if __name__ == "__main__":
    main()
