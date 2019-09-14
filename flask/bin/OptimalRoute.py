"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import DistanceMatrix

def create_data_model(destinations, depot, num_vehicles):
    """Stores the data for the problem."""
    data = {}
    if destinations:
        data['distance_matrix'] = DistanceMatrix.get_distance_matrix(destinations)
    else:
        data['distance_matrix'] =    [[0, 24357, 33350, 14928, 31957, 32166, 19319, 28392, 15556, 21404, 28731, 34765, 35142, 10523, 26727, 26303], 
                        [25244, 0, 8314, 11334, 6922, 7131, 10678, 3270, 11257, 7873, 11350,9729, 10107, 19122, 12350, 13609], 
                        [34062, 8491, 0, 13999, 4086, 1651, 11008, 4239, 13715, 9541, 7179, 1864, 925, 27939, 9730, 9997], 
                        [15494, 10991, 13938, 0, 11065, 12745, 4047, 10970, 581, 5226, 10788, 15681, 16059, 6012, 9180, 9401], 
                        [33351, 5882, 4096, 11348, 0, 2671, 7580, 4363, 11064, 6736, 3642, 5108, 5485, 20768, 6649, 7072], 
                        [32869, 7298, 1665, 12806, 2893, 0, 9815, 3840, 12522, 8348, 6298, 2762, 2479, 26746, 8848, 9462], 
                        [19361, 10638, 11017, 4038, 7398, 9834, 0, 9159, 3754, 2809, 7099, 10921, 13146, 9186, 5491, 5879], 
                        [29097, 3270, 4257, 11458, 4350, 3848, 9159, 0, 11174, 6354, 9303, 5359, 5151, 22975, 10620, 11562], 
                        [15809, 10707, 13654, 581, 10782, 12461, 3763, 10687, 0, 4943, 10504, 15398, 15775,5432, 8896, 9117],
                        [21831, 7911, 9406, 5226, 6282, 8213, 2809, 6354, 4943, 0, 6967, 11149, 11526, 10374, 5119, 6383], 
                        [28822, 11931, 6831, 10681, 3281, 5965, 6999, 10627, 10397, 7159, 0, 5693, 6422, 18297, 3267, 4068], 
                        [35492, 9921, 1824, 15581, 5023, 2353, 10856, 5438, 15297, 11123, 5964, 0, 1394, 29415, 8515, 8782],
                        [36058, 10487, 927, 16148, 5590, 2468, 13242, 9183, 15864, 11689, 6734, 1506, 0, 29982, 9285, 9552],
                        [11333, 19346, 28339, 6012, 20917, 27155, 9194, 23381, 5432, 10374, 18568, 29458, 29835, 0, 16564, 16140],
                        [27151, 11444, 9719, 10131, 6656, 8853, 5827, 10421, 9847, 5455, 3335, 8581, 9309, 16626, 0, 1264],
                        [27464, 14469, 10618, 9394, 7017, 9676, 5879, 13164, 9110, 6422, 3933, 9481, 10209, 16939, 1288, 0]]


    data['num_vehicles'] = num_vehicles
    data['depot'] = depot
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    result = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        result.append([])
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            result[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        result[vehicle_id].append(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    return result

def google_maps_string(stops):
    query = "https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}&travelmode=car"
    origin = stops[0]
    destination = stops[-1]
    stopovers = stops[1:-1]
    print(stopovers)
    return query.format(origin,destination,'|'.join(stopovers))

def main():
    get_optimal_route()

def get_optimal_route(destinations = None, depot = 0, num_vehicles = 1):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(destinations,depot,num_vehicles)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        70000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        result = print_solution(data, manager, routing, solution)
        
    return result



if __name__ == '__main__':
    main()