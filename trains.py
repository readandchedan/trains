def build_gragh(graph_string):
    """
    A quick parser from string into a dict that represent the graph.
    Keys in the root level are the start of the path, keys in the result
    are the desinations, values are the distance of the path
    sample format:
    AB5, BC4
    returns {"A": {"B": 5}, "B": {"C": 4}}
    """
    graph = {}
    routes = [i.strip() for i in graph_string.split(',')]
    for r in routes:
        start, end, weight = r
        weight = int(weight)
        if start not in graph:
            graph[start] = {end: weight}
        else:
            graph[start][end] = weight

    return graph


def split_routes(route):
    """
    just a quick helper function that split
    [node1, node2, node3, node4 ...]
    to
    [[node1, node2], [node2, node3], [node3, node4], ...]
    easier to get node distance easier.
    there are perhaps better way to do this
    """
    routes = []
    for i in range(0, len(route)):
        if i + 2 <= len(route):
            routes.append(route[i:i+2])
    return routes


def calculate_distance(graph, route):
    """
    calculate the distance by following a given route,
    if there's path, return 'NO SUCH ROUTE'
    else return the distance following the route
    """
    distance = 0
    routes = split_routes(route)
    for r in routes:
        start, end = r
        d = graph.get(start, {}).get(end)
        if d is None:
            return "NO SUCH ROUTE"
        else:
            distance += d
    return distance


def _find_paths(graph, start, end, paths, paths_so_far=""):
    """
    Recursive helper function for finding paths.
    Given graph, a start and an end, return all the path can be found.
    This is done by tracking if the current path have the specified start
    and end point, if not then keep looking.
    This version allows the start and end to be the same point,
    but won't include cycles.
    """
    paths_so_far += start
    for node in graph.get(start, {}):
        if node == end:
            paths.append(paths_so_far + node)
        elif node not in paths_so_far:
            _find_paths(graph, node, end, paths, paths_so_far)


def find_paths(graph, start, end):
    """
    Wrapper function to find all paths, for easier use.
    Given graph, start and end point, return all found paths that doesn't
    include cycles.
    """
    paths = []
    _find_paths(graph, start, end, paths)
    return paths


# this is a lazy way of doing this, but since the problem requires check all
# the path at least once, this should do.
def find_shortest_path(graph, start, end):
    """
    Given a graph, start and end point, return the shortest path
    """
    paths = find_paths(graph, start, end)
    if not paths:
        return -1
    return min([calculate_distance(graph, p) for p in paths])


# the idea of this function was to find all the paths that are with at most
# x stops. This is done by don't stop looking for paths unless the path is
# already longer than the required length. Also, when found anything, add in
# to the found path. This is different than finding shortest path.
#
# To handle the case that includes cycles, the boundry condition
# are made wider than it should be, allowing filters to get all the required
# paths. This can be improved.
def _find_paths_with_length(graph, start, end, length, paths, paths_so_far=""):
    """
    Helper recursive function for finding all paths given a start, and end
    a graph, and the specific number of stops.
    """
    paths_so_far += start
    for node in graph.get(start, {}):
        length_so_far = len(paths_so_far)
        # when the path is still shorter than required length, keep looking
        if length_so_far < length:
            _find_paths_with_length(graph, node, end, length, paths,
                                    paths_so_far)

        # but if something was found, add them in anyway
        if node == end:
            paths.append(paths_so_far + node)


def find_paths_with_lte_stops(graph, start, end, stop):
    """
    Wrapper of the helper function, given graph, start, end, and stops
    returns all the paths that have less than or euqal to the stops given
    """
    paths = []
    length = stop + 1
    # a path with x stop is actually of length stop + 1
    _find_paths_with_length(graph, start, end, length, paths)
    return filter(lambda r: len(r) <= length, paths)


def find_paths_with_eq_stops(graph, start, end, stop):
    """
    Wrapper of the helper function, given graph, start, end, and stops
    returns all the paths that have less than or euqal to the stops given
    """
    paths = []
    length = stop + 1
    # a path with x stop is actually of length stop + 1
    _find_paths_with_length(graph, start, end, length, paths)
    return filter(lambda r: len(r) == length, paths)


# Like the path finding function with stops, this function as well returns a
# broarder restuls than required, to handle cycles. This can also perhaps be
# improved.
def _find_paths_with_distance(graph, start, end, distance, paths,
                              paths_so_far=""):
    """
    Similar recursive function that returns the paths with specific distance,
    given a graph, a start and a end point.
    """
    paths_so_far += start
    for node in graph.get(start, {}):
        distance_so_far = calculate_distance(graph, paths_so_far)
        # if current distance is still less than required distance,
        # keep looking
        if distance_so_far < distance:
            _find_paths_with_distance(graph, node, end, distance, paths,
                                      paths_so_far)
        # however, if any paths was already find, add them in to path as well
        if node == end:
            paths.append(paths_so_far + node)


def find_paths_with_lt_distance(graph, start, end, distance):
    """
    Wrapper of the helper function, given graph, start, end, and asked distance
    return paths and their distance that are less than distance given
    """
    paths = []
    _find_paths_with_distance(graph, start, end, distance, paths)
    paths_distance = []
    for p in paths:
        d = calculate_distance(graph, p)
        if d < distance:
            paths_distance.append(p)
    return paths_distance
