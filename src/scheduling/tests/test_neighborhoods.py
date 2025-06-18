import unittest
import os
from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.optim.neighborhoods import MachineSwitchNeighborhood, OperationOrderNeighborhood
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA



def create_initial_solution():
    inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_test_neighborhoods")
    solution = Solution(inst)

    # Planifier plusieurs opérations sur différentes machines
    operations_to_schedule = [
        (0, 0), (0, 1), (0, 2),  # Job 0
        (1, 3), (1, 4), (1, 5),  # Job 1
        (2, 6), (2, 7), (2, 8)   # Job 2
    ]

    for job_id, op_id in operations_to_schedule:
        operation = next(op for op in inst.operations
                       if op.job_id == job_id and op.operation_id == op_id)
        machine = inst.machines[0]
        solution.schedule(operation, machine)

    return inst, solution

class TestNeighborhoods(unittest.TestCase):

    def test_machine_switch_best_neighbor(self):
        """Tester la recherche du meilleur voisin pour MachineSwitchNeighborhood"""
        inst, solution = create_initial_solution()
        neighborhood = MachineSwitchNeighborhood(inst)
        initial_value = solution.evaluate
        
        best_sol = neighborhood.best_neighbor(solution)
        
        self.assertLessEqual(best_sol.evaluate, initial_value)
        self.assertTrue(best_sol.is_feasible)

        
    def test_operation_order_best_neighbor(self):
        """Tester la recherche du meilleur voisin pour OperationOrderNeighborhood"""
        inst, solution = create_initial_solution()
        neighborhood = OperationOrderNeighborhood(inst)
        initial_value = solution.evaluate
        
        best_sol = neighborhood.best_neighbor(solution)
        
        self.assertLessEqual(best_sol.evaluate, initial_value)
        self.assertTrue(best_sol.is_feasible)
        
    def test_machine_switch_first_better(self):
        """Tester la recherche du premier voisin améliorant pour MachineSwitchNeighborhood"""
        inst, solution = create_initial_solution()
        neighborhood = MachineSwitchNeighborhood(inst)
        initial_value = solution.evaluate
        
        better_sol = neighborhood.first_better_neighbor(solution)
        
        self.assertLessEqual(better_sol.evaluate, initial_value)
        self.assertTrue(better_sol.is_feasible)
        
    def test_operation_order_first_better(self):
        """Tester la recherche du premier voisin améliorant pour OperationOrderNeighborhood"""
        # Planifier une deuxième opération sur la même machine
        inst, solution = create_initial_solution()
        neighborhood = OperationOrderNeighborhood(inst)
        initial_value = solution.evaluate
        
        better_sol = neighborhood.first_better_neighbor(solution)
        
        self.assertLessEqual(better_sol.evaluate, initial_value)
        self.assertTrue(better_sol.is_feasible)

if __name__ == '__main__':
    unittest.main()