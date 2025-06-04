'''
Tests for the Machine class

@author: Vassilissa Lehoux
'''
import unittest
from src.scheduling.instance.machine import Machine
from src.scheduling.instance.operation import Operation

class TestMachine(unittest.TestCase):

    def setUp(self):
        self.machine = Machine(0, 1, 2, 3, 4, 5, 100)
        # Création de deux opérations fictives
        op1 = Operation(0, 0)
        op2 = Operation(1, 0)
        # On simule leur planification
        op1._schedule_info = type('Schedule', (), {'schedule_time': 0, 'duration': 5, 'energy_consumption': 2, 'assigned_to': 0})()
        op2._schedule_info = type('Schedule', (), {'schedule_time': 5, 'duration': 7, 'energy_consumption': 3, 'assigned_to': 0})()
        self.machine._scheduled_operations.append(op1)
        self.machine._scheduled_operations.append(op2)
        # On simule un démarrage et un arrêt
        self.machine._start_times.append(0)
        self.machine._stop_times.append(12)

    def tearDown(self):
        pass

    def testWorkingTime(self):
        self.assertEqual(self.machine.working_time, 12, "Le temps de travail devrait être 12")

    def testTotalEnergyConsumption(self):
        # 2+3 (opérations) + 1*2 (set_up) + 1*4 (tear_down)
        self.assertEqual(self.machine.total_energy_consumption, 11, "La consommation totale devrait être 11")

if __name__ == "__main__":
    unittest.main()