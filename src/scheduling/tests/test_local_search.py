import copy
import os
import unittest

from src.scheduling.instance.instance import Instance
from src.scheduling.optim.constructive import NonDeterminist
from src.scheduling.optim.local_search import FirstNeighborLocalSearch
from src.scheduling.optim.neighborhoods import MachineSwitchNeighborhood
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA



class TestLocalSearch(unittest.TestCase):
    def setUp(self):
        self.instance = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_easy")
        self.non_det = NonDeterminist()
        self.neigh = MachineSwitchNeighborhood(self.instance)
        self.local_search = FirstNeighborLocalSearch()
        self.instance_copy_test_1 = copy.deepcopy(self.instance)
        self.instance_copy_test_2 = copy.deepcopy(self.instance)


    def test_first_neighbor_local_search_improves_or_equals(self):


        # Génère une solution initiale non déterministe
        initial_solution = self.non_det.run(self.instance)
        initial_eval = initial_solution.evaluate


        # Applique la recherche locale
        improved_solution = self.local_search.run(self.instance_copy_test_1, self.non_det, self.neigh)
        improved_eval = improved_solution.evaluate

        # La solution retournée doit être faisable
        self.assertTrue(improved_solution.is_feasible)
        # La solution retournée doit être au moins aussi bonne que l'initiale
        self.assertLessEqual(improved_eval, initial_eval)

    def test_first_neighbor_local_search_repeatability(self):
        # Plusieurs runs doivent donner des solutions faisables
        for _ in range(5):
            sol = self.local_search.run(self.instance_copy_test_2, self.non_det, self.neigh)
            self.assertTrue(sol.is_feasible)
            self.assertIsInstance(sol.evaluate, int)

if __name__ == "__main__":
    unittest.main()