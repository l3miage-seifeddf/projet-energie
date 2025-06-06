'''
Constructive heuristics that returns preferably **feasible** solutions.

@author: Vassilissa Lehoux
'''
from typing import Dict
import random

from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.optim.heuristics import Heuristic


def _evaluate_cost(operation, machine) -> float:
    '''
    Evaluates the cost of assigning an operation to a machine.
    Cost can be based on energy consumption or duration.
    '''
    energy_cost = operation.energies[machine.machine_id]
    duration_cost = operation.processing_times[machine.machine_id]
    return energy_cost + duration_cost


class Greedy(Heuristic):
    '''
    A deterministic greedy method to return a solution.
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        self.params = params

    def run(self, instance: Instance, params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param params: the parameters for the run
        '''
        solution = Solution(instance)
        for job in instance.jobs:
            for operation in job.operations:
                best_machine = None
                best_cost = float('inf')
                for machine in instance.machines:
                    cost = _evaluate_cost(operation, machine)
                    if cost < best_cost:
                        best_cost = cost
                        best_machine = machine
                if best_machine:
                    solution.schedule(operation, best_machine)
        return solution


class NonDeterminist(Heuristic):
    '''
    Heuristic that returns different values for different runs with the same parameters
    (or different values for different seeds and otherwise same parameters)
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        self.params = params

    def run(self, instance: Instance, params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param params: the parameters for the run
        '''
        solution = Solution(instance)
        for job in instance.jobs:
            for operation in job.operations:
                feasible_machines = [machine for machine in instance.machines if
                                     machine.available_time <= operation.min_start_time]
                if feasible_machines:
                    selected_machine = random.choice(feasible_machines)
                    solution.schedule(operation, selected_machine)
        return solution


if __name__ == "__main__":
    # Example of playing with the heuristics
    from src.scheduling.tests.test_utils import TEST_FOLDER_DATA
    import os
    inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")
    heur = NonDeterminist()
    sol = heur.run(inst)
    plt = sol.gantt("tab20")
    plt.savefig("gantt.png")
