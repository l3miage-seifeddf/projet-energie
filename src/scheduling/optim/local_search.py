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

    def run(self, instance, params: Dict = dict()) -> Solution:
        self.nonDeterminist = params['nonDeterminist']
        self.machineSwitchNeighborhood = params['machineSwitchNeighborhood']
        # Génère une solution initiale
        current_solution = self.nonDeterminist.run(instance)

        improved = True

        while improved:
            improved = False

            current_solution_copy = copy.deepcopy(current_solution)

            neighbor_solution = self.machineSwitchNeighborhood.first_better_neighbor(current_solution_copy)

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


    def run(self, instance: Instance, params: Dict=dict()) -> Solution:
        '''
        Computes a solution for the given instance.
        Implementation should provide default values in the function
        (the function will be evaluated with an empty dictionary).

        @param instance: the instance to solve
        @param InitClass: the class for the heuristic computing the initialization
        @param NeighborClass: the class of neighborhood used in the vanilla local search
        @param params: the parameters for the run
        '''
        self.nonDeterminist = params['nonDeterminist']
        self.machineSwitchNeighborhood = params['machineSwitchNeighborhood']
        self.operationOrderNeighborhood = params['operationOrderNeighborhood']
        current_solution = self.nonDeterminist.run(instance)

        first_solution = copy.deepcopy(current_solution)

        first_neighbor_solution = self.machineSwitchNeighborhood.best_neighbor(first_solution)

        second_solution = copy.deepcopy(first_solution)

        second_neighbor_solution = self.operationOrderNeighborhood.best_neighbor(second_solution)

        if second_neighbor_solution.evaluate < first_neighbor_solution.evaluate:
            current_solution = second_neighbor_solution
        else:
            current_solution = first_neighbor_solution

        return current_solution




if __name__ == "__main__":
    # To play with the heuristics
    from src.scheduling.tests.test_utils import TEST_FOLDER_DATA
    import os
    inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")
    nondeterminist = NonDeterminist()
    machineSwitchNeighborhood = MachineSwitchNeighborhood(inst)
    operationOrderNeighborhood = OperationOrderNeighborhood(inst)

    params1 = {
        'nonDeterminist': nondeterminist,
        'machineSwitchNeighborhood': machineSwitchNeighborhood
    }
    heur1 = FirstNeighborLocalSearch()
    sol1 = heur1.run(inst, params1)
    plt1 = sol1.gantt("tab20")
    plt1.savefig("../img/gantt1.png")

    params2 = {
        'nonDeterminist': nondeterminist,
        'machineSwitchNeighborhood': machineSwitchNeighborhood,
        'operationOrderNeighborhood': operationOrderNeighborhood
    }
    heur2 = BestNeighborLocalSearch()
    sol2 = heur2.run(inst, params2)
    plt2 = sol2.gantt("tab20")
    plt2.savefig("../img/gantt2.png")
