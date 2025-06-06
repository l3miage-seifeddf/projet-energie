'''
Neighborhoods for solutions.
They must derive from the Neighborhood class.

@author: Vassilissa Lehoux
'''
import copy
from typing import Dict

from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution


class Neighborhood(object):
    '''
    Base neighborhood class for solutions of a given instance.
    Do not modify!!!
    '''

    def __init__(self, instance: Instance, params: Dict=dict()):
        '''
        Constructor
        '''
        self._instance = instance

    def best_neighbor(self, sol: Solution) -> Solution:
        '''
        Returns the best solution in the neighborhood of the solution.
        Can be the solution itself.
        '''
        raise "Not implemented error"

    def first_better_neighbor(self, sol: Solution):
        '''
        Returns the first solution in the neighborhood of the solution
        that improves other it and the solution itself if none is better.
        '''
        raise "Not implemented error"


class MachineSwitchNeighborhood(Neighborhood):
    '''
    Premier voisinage : change la machine sur laquelle s'exécute une opération.
    Taille du voisinage : O(O * (M-1)) où O est le nombre d'opérations et M le nombre de machines.
    '''

    def __init__(self, instance: Instance, params: Dict=dict()):
        '''
        Constructor
        '''
        super().__init__(instance,params)

    def best_neighbor(self, sol: Solution) -> Solution:
        '''
        Returns the best solution in the neighborhood of the solution.
        Can be the solution itself.
        '''
        best_solution = sol
        best_value = sol.evaluate

        for operation in sol.all_operations:
            current_machine_id = operation.assigned_to
            for machine in self._instance.machines:
                if machine.machine_id != current_machine_id:
                    # Créer une nouvelle solution
                    neighbor = copy.deepcopy(sol)
                    # Trouver l'opération correspondante dans la nouvelle solution
                    op = next(op for op in neighbor.all_operations if op.operation_id == operation.operation_id)
                    # Réassigner l'opération à la nouvelle machine
                    op.reset()
                    neighbor.schedule(op, machine)

                    # Évaluer le voisin
                    neighbor_value = neighbor.evaluate
                    if neighbor_value < best_value:
                        best_solution = neighbor
                        best_value = neighbor_value

        return best_solution

    def first_better_neighbor(self, sol: Solution) -> Solution:
        '''
        Returns the first solution in the neighborhood of the solution
        that improves other it and the solution itself if none is better.
        '''
        current_value = sol.evaluate

        for operation in sol.all_operations:
            current_machine_id = operation.assigned_to
            for machine in self._instance.machines:
                if machine.machine_id != current_machine_id:
                    # Créer une nouvelle solution
                    neighbor = copy.deepcopy(sol)
                    # Trouver l'opération correspondante dans la nouvelle solution
                    op = next(op for op in neighbor.all_operations if op.operation_id == operation.operation_id)
                    # Réassigner l'opération à la nouvelle machine
                    op.reset()
                    neighbor.schedule(op, machine)

                    # Si le voisin est meilleur, le retourner immédiatement
                    if neighbor.evaluate < current_value:
                        return neighbor

        return sol



class OperationOrderNeighborhood(Neighborhood):
    '''
    Deuxième voisinage : Permutations d'ordre sur une machine.
    Taille du voisinage : O(N^2) dans le pire cas, où N est le nombre total d'opérations.
    '''


    def __init__(self, instance: Instance, params: Dict=dict()):
        '''
        Constructor
        '''
        super().__init__(instance, params)

    def best_neighbor(self, sol: Solution) -> Solution:
        '''
        Returns the best solution in the neighborhood of the solution.
        Can be the solution itself.
        '''
        best_solution = sol
        best_value = sol.evaluate

        for machine in self._instance.machines:
            # Récupérer toutes les opérations sur cette machine
            machine_ops = [op for op in sol.all_operations if op.assigned_to == machine.machine_id]

            # Pour chaque paire d'opérations sur la machine
            for i in range(len(machine_ops)):
                for j in range(i + 1, len(machine_ops)):
                    # Créer une nouvelle solution
                    neighbor = _create_neighbor_solution(sol, machine_ops[i], machine_ops[j], machine)

                    # Évaluer le voisin
                    neighbor_value = neighbor.evaluate
                    if neighbor_value < best_value:
                        best_solution = neighbor
                        best_value = neighbor_value

        return best_solution

    def first_better_neighbor(self, sol: Solution) -> Solution:
        '''
        Returns the first solution in the neighborhood of the solution
        that improves other it and the solution itself if none is better.
        '''
        current_value = sol.evaluate

        for machine in self._instance.machines:
            # Récupérer toutes les opérations sur cette machine
            machine_ops = [op for op in sol.all_operations if op.assigned_to == machine.machine_id]

            # Pour chaque paire d'opérations sur la machine
            for i in range(len(machine_ops)):
                for j in range(i + 1, len(machine_ops)):
                    # Créer une nouvelle solution
                    neighbor = _create_neighbor_solution(sol, machine_ops[i], machine_ops[j], machine)

                    # Si le voisin est meilleur, le retourner immédiatement
                    if neighbor.evaluate < current_value:
                        return neighbor

        return sol


def _create_neighbor_solution(sol: Solution, op1, op2, machine):
    '''
    Helper function to create a neighbor solution by swapping two operations.
    '''
    neighbor = copy.deepcopy(sol)

    # Trouver les opérations correspondantes dans la nouvelle solution
    op1_neighbor = next(op for op in neighbor.all_operations if op.operation_id == op1.operation_id)
    op2_neighbor = next(op for op in neighbor.all_operations if op.operation_id == op2.operation_id)

    # Réinitialiser les assignations
    op1_neighbor.reset()
    op2_neighbor.reset()

    # Réassigner les opérations dans l'ordre inverse
    neighbor.schedule(op2_neighbor, machine)
    neighbor.schedule(op1_neighbor, machine)

    return neighbor
