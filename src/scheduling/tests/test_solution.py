'''
Test of the Solution class.

@author: Vassilissa Lehoux
'''
import os
import unittest

from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.tests.test_utils import TEST_FOLDER, TEST_FOLDER_DATA


class TestSolution(unittest.TestCase):

    def setUp(self):
        self.inst1 = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")

    def tearDown(self):
        pass

    def test_init_sol(self):
        sol = Solution(self.inst1)
        self.assertEqual(len(sol.all_operations), len(self.inst1.operations),
                         'Nb of operations should be the same between instance and solution')
        self.assertEqual(len(sol.available_operations), len(self.inst1.jobs),
                         'One operation per job should be available for scheduling')

    def test_schedule_op(self):
        sol = Solution(self.inst1)
        operation = self.inst1.operations[0]
        machine = self.inst1.machines[1]
        sol.schedule(operation, machine)
        self.assertEqual(operation.assigned, True, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 1, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 12, 'wrong operation duration')
        self.assertEqual(operation.energy, 12, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 20, 'wrong set up time for machine')
        self.assertEqual(operation.end_time, 32, 'wrong operation end time')
        self.assertEqual(machine.available_time, 32, 'wrong available time')
        self.assertEqual(machine.working_time, 120, 'wrong working time for machine')
        operation = self.inst1.operations[2]
        sol.schedule(operation, machine)
        self.assertEqual(operation.assigned, True, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 1, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 9, 'wrong operation duration')
        self.assertEqual(operation.energy, 10, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 32, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 41, 'wrong operation end time')
        self.assertEqual(machine.available_time, 41, 'wrong available time')
        self.assertEqual(machine.working_time, 120, 'wrong working time for machine')
        operation = self.inst1.operations[1]
        machine = self.inst1.machines[0]
        sol.schedule(operation, machine)
        self.assertEqual(operation.assigned, True, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 0, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 5, 'wrong operation duration')
        self.assertEqual(operation.energy, 6, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 32, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 37, 'wrong operation end time')
        self.assertEqual(machine.available_time, 37, 'wrong available time')
        self.assertEqual(machine.working_time, 83, 'wrong working time for machine')
        self.assertEqual(machine.start_times[0], 17)
        self.assertEqual(machine.stop_times[0], 100)
        operation = self.inst1.operations[3]
        sol.schedule(operation, machine)
        self.assertEqual(operation.assigned, True, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 0, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 10, 'wrong operation duration')
        self.assertEqual(operation.energy, 9, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 41, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 51, 'wrong operation end time')
        self.assertEqual(machine.available_time, 51, 'wrong available time')
        self.assertEqual(machine.working_time, 83, 'wrong working time for machine')
        self.assertEqual(machine.start_times[0], 17)
        self.assertEqual(machine.stop_times[0], 100)
        self.assertTrue(sol.is_feasible, 'Solution should be feasible')
        plt = sol.gantt('tab20')
        plt.savefig(TEST_FOLDER + os.path.sep +  'temp.png')
        sol.to_csv()

    def test_objective(self):
        '''
        Test your objective function
        '''
        inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_minimal")
        sol = Solution(inst)
        operation = inst.operations[0]
        machine = inst.machines[0]
        sol.schedule(operation, machine)

        self.assertTrue(operation.assigned)
        self.assertEqual(operation.processing_time, 5)
        self.assertEqual(operation.energy, 10)
        self.assertEqual(operation.start_time, 0)
        self.assertEqual(operation.end_time, 5)

        # Calcul attendu :
        # total_energy_consumption = 10 (juste l'opération, pas de setup/teardown/min)
        # cmax = 5 (fin de l'opération)
        # mean_processing_time = 5 (1 job, 1 opération)
        # objective = 10 + 5 + 5 = 20
        self.assertEqual(sol.objective, 20, "Objective should be 20 for this minimal instance")

    def test_evaluate(self):
        '''
        Test your evaluate function
        '''
        inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp_minimal")
        sol_unfeasible = Solution(inst)
        eval_unfeasible = sol_unfeasible.evaluate
        self.assertFalse(sol_unfeasible.is_feasible)
        self.assertTrue(eval_unfeasible > 100000, "Unfeasible solution should be heavily penalized")

        sol_feasible = Solution(inst)
        operation = inst.operations[0]
        machine = inst.machines[0]
        sol_feasible.schedule(operation, machine)
        eval_feasible = sol_feasible.evaluate
        self.assertTrue(sol_feasible.is_feasible)
        self.assertEqual(eval_feasible, sol_feasible.objective)




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
