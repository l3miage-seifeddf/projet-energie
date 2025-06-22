'''
Heuristics that compute an initial solution and 
then improve it.

@author: Vassilissa Lehoux
'''
import copy
from typing import Dict

from src.scheduling.optim.heuristics import Heuristic
from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.optim.constructive import NonDeterminist
from src.scheduling.optim.neighborhoods import MachineSwitchNeighborhood
from src.scheduling.optim.neighborhoods import OperationOrderNeighborhood



class FirstNeighborLocalSearch(Heuristic):
    '''
    Vanilla local search will first create a solution,
    then at each step try and improve it by looking at
    solutions in its neighborhood.
    The first solution found that improves over the current solution
    replaces it.
    The algorithm stops when no solution is better than the current solution
    in its neighborhood.
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        self.params = params

    def run(self, instance: Instance, nonDeterminist: NonDeterminist,
            machineSwitchNeighborhood: MachineSwitchNeighborhood, params: Dict = dict()) -> Solution:
        # Génère une solution initiale
        current_solution = nonDeterminist.run(instance)

        improved = True

        while improved:
            improved = False

            current_solution_copy = copy.deepcopy(current_solution)

            neighbor_solution = machineSwitchNeighborhood.first_better_neighbor(current_solution_copy)

            if neighbor_solution.evaluate < current_solution.evaluate:
                current_solution = neighbor_solution
                improved = True

        return current_solution


class BestNeighborLocalSearch(Heuristic):
    '''
    Vanilla local search will first create a solution,
    then at each step try and improve it by looking at
    solutions in its neighborhood.
    The best solution found that improves over the current solution
    replaces it.
    The algorithm stops when no solution is better than the current solution
    in its neighborhood.
    '''

    def __init__(self, params: Dict=dict()):
        '''
        Constructor
        @param params: The parameters of your heuristic method if any as a
               dictionary. Implementation should provide default values in the function.
        '''
        self.params = params

    def run(self, instance: Instance, nonDeterminist: NonDeterminist,
            operationOrderNeighborhood: OperationOrderNeighborhood,
            machineSwitchNeighborhood: MachineSwitchNeighborhood,
            params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param InitClass: the class for the heuristic computing the initialization
        @param NeighborClass: the class of neighborhood used in the vanilla local search
        @param params: the parameters for the run
        '''
        current_solution = nonDeterminist.run(instance)

        first_solution = copy.deepcopy(current_solution)

        first_neighbor_solution = machineSwitchNeighborhood.best_neighbor(first_solution)

        second_solution = copy.deepcopy(first_solution)

        second_neighbor_solution = operationOrderNeighborhood.best_neighbor(second_solution)

        if second_neighbor_solution.evaluate < first_neighbor_solution.evaluate:
            current_solution = second_neighbor_solution
        else:
            current_solution = first_neighbor_solution

        return current_solution




if __name__ == "__main__":
    # To play with the heuristics
    from src.scheduling.tests.test_utils import TEST_FOLDER_DATA
    import os
    inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp10")
    heur = FirstNeighborLocalSearch()
    sol = heur.run(inst, NonDeterminist, MachineSwitchNeighborhood)
    plt = sol.gantt("tab20")
    plt.savefig("gantt.png")
