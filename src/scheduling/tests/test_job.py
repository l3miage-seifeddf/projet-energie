'''
Tests for the Job class

@author: Vassilissa Lehoux
'''
import unittest
from src.scheduling.instance.job import Job
from src.scheduling.instance.operation import Operation

class TestJob(unittest.TestCase):

    def setUp(self):
        self.job = Job(0)
        # Création de deux opérations fictives
        op1 = Operation(0, 0)
        op2 = Operation(0, 1)
        # On simule leur planification
        op1._schedule_info = type('Schedule', (), {'schedule_time': 0, 'duration': 5, 'energy_consumption': 2, 'assigned_to': 1})()
        op2._schedule_info = type('Schedule', (), {'schedule_time': 5, 'duration': 7, 'energy_consumption': 3, 'assigned_to': 2})()
        self.job.add_operation(op1)
        self.job.add_operation(op2)

    def tearDown(self):
        pass

    def testCompletionTime(self):
        # Le temps de complétion doit être la fin de la dernière opération
        self.assertEqual(self.job.completion_time, 12, "Le temps de complétion devrait être 12 (5+7)")

if __name__ == "__main__":
    unittest.main()
