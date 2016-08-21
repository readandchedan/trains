import unittest
from trains import (
    build_gragh,
    split_routes,
    calculate_distance,
    find_paths,
    find_shortest_path,
    find_paths_with_eq_stops,
    find_paths_with_lte_stops,
    find_paths_with_lt_distance
)


class UnitTest(unittest.TestCase):

    def test_build_gragh(self):
        graph_str = "AB5, BC8, AC4"
        graph = build_gragh(graph_str)
        self.assertTrue('A' in graph)
        self.assertTrue('B' in graph)
        self.assertTrue('B' in graph['A'])
        self.assertTrue('C' in graph['A'])
        self.assertTrue('C' in graph['B'])
        self.assertTrue(graph['A']['B'] == 5)
        self.assertTrue(graph['B']['C'] == 8)
        self.assertTrue(graph['A']['C'] == 4)

    def test_split_routes(self):
        path = "ABCDE"
        p = split_routes(path)
        expected = ["AB", "BC", "CD", "DE"]
        self.assertTrue(len(p) == len(expected))
        for i, e in enumerate(expected):
            self.assertTrue(e == p[i])

    def test_calculate_distance(self):
        graph_str = "AB5, BC8"
        graph = build_gragh(graph_str)

        d = calculate_distance(graph, "AB")
        self.assertTrue(d == 5)

        d = calculate_distance(graph, "ABC")
        self.assertTrue(d == 13)

    def test_calculate_distance_no_route(self):
        graph_str = "AB5, BC8"
        graph = build_gragh(graph_str)
        d = calculate_distance(graph, "AE")
        self.assertTrue(d == "NO SUCH ROUTE")

    def test_find_paths(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        paths = find_paths(graph, 'A', 'C')
        self.assertTrue('ABC' in paths)
        self.assertTrue('AC' in paths)

    def test_find_no_paths(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        paths = find_paths(graph, 'C', 'B')
        self.assertTrue(len(paths) == 0)

    def test_shortest_path(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        shortest = find_shortest_path(graph, 'A', 'C')
        self.assertTrue(shortest == 5)

    def test_no_shortest_path(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        shortest = find_shortest_path(graph, 'C', 'B')
        self.assertTrue(shortest == -1)

    def test_find_paths_with_lte_stops(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        paths = find_paths_with_lte_stops(graph, 'A', 'C', 2)
        self.assertTrue('AC' in paths)
        self.assertTrue('ABC' in paths)
        self.assertTrue(len(paths) == 2)

        paths = find_paths_with_eq_stops(graph, 'A', 'C', 1)
        self.assertTrue('AC' in paths)
        self.assertTrue(len(paths) == 1)

    def test_find_paths_with_lt_distance(self):
        graph_str = "AB5, BC8, AC5"
        graph = build_gragh(graph_str)
        path_distances = find_paths_with_lt_distance(graph, 'A', 'C', 14)
        self.assertTrue('AC' in path_distances)
        self.assertTrue('ABC' in path_distances)

if __name__ == '__main__':
    unittest.main()
