'''
Tests for the Heuristics

@author: Farah Seifeddine et Léo Bouvier
'''
import os
import unittest

from src.scheduling.instance.instance import Instance
from src.scheduling.optim.constructive import Greedy, NonDeterminist
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA


class TestConstructive(unittest.TestCase):

    def setUp(self):
        self.instance = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_easy")
        self.instance2 = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_easy")

    def tearDown(self):
        pass

    def testGreedy(self):
        heuristic = Greedy()
        first_solution = heuristic.run(self.instance)
        second_solution = heuristic.run(self.instance2)
        self.assertEqual(first_solution.evaluate, second_solution.evaluate, "Les solutions ne sont pas égales")
        self.assertEqual(first_solution.evaluate, 29, "Les solutions ne sont pas égales")
        self.assertTrue(first_solution.is_feasible)

    def testNonDeterminist(self):
        heuristic = NonDeterminist()
        first_solution = heuristic.run(self.instance)
        second_solution = heuristic.run(self.instance2)
        self.assertNotEqual(first_solution.evaluate, second_solution.evaluate, "Les solutions sont égales")
        self.assertTrue(first_solution.is_feasible)
        self.assertTrue(second_solution.is_feasible)


if __name__ == "__main__":
    unittest.main()
