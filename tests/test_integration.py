import unittest
from trains import (
    build_gragh,
    split_routes,
    calculate_distance,
    find_paths,
    find_shortest_path,
    find_paths_with_lte_stops,
    find_paths_with_eq_stops,
    find_paths_with_lt_distance
)


class UnitTest(unittest.TestCase):

    def setUp(self):
        graph_string = "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7"
        self.graph = build_gragh(graph_string)

    def test_q1_to_q5(self):
        graph_str = "AB5, BC8, AC4"
        graph = build_gragh(graph_str)
        # 1
        self.assertTrue(calculate_distance(self.graph, "ABC") == 9)
        # 2
        self.assertTrue(calculate_distance(self.graph, "AD") == 5)
        # 3
        self.assertTrue(calculate_distance(self.graph, "ADC") == 13)
        # 4
        self.assertTrue(calculate_distance(self.graph, "AEBCD") == 22)
        # 5
        self.assertTrue(
            calculate_distance(self.graph, "AED") == "NO SUCH ROUTE"
        )

    def test_q6(self):
        paths = find_paths_with_lte_stops(self.graph, "C", "C", 3)
        self.assertTrue('CEBC' in paths)
        self.assertTrue('CDC' in paths)
        self.assertTrue(len(paths) == 2)

    def test_q7(self):
        paths = find_paths_with_eq_stops(self.graph, "A", "C", 4)
        self.assertTrue('ABCDC' in paths)
        self.assertTrue('ADEBC' in paths)
        self.assertTrue('ADCDC' in paths)
        self.assertTrue(len(paths) == 3)

    def test_q8(self):
        self.assertTrue(find_shortest_path(self.graph, "A", "C") == 9)

    def test_q9(self):
        self.assertTrue(find_shortest_path(self.graph, "B", "B") == 9)

    def test_q10(self):
        paths = find_paths_with_lt_distance(self.graph, 'C', 'C', 30)
        expected = ['CDC', 'CEBC', 'CEBCDC', 'CDCEBC', 'CDEBC', 'CEBCEBC',
                    'CEBCEBCEBC']
        self.assertTrue(len(paths) == 7)
        for e in expected:
            self.assertTrue(e in paths)

if __name__ == '__main__':
    unittest.main()
