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
                    # we need to remove the operation from the current machine
                    current_machine = next((m for m in neighbor.inst.machines if m.machine_id == current_machine_id), None)
                    if current_machine is not None:
                        current_machine.remove_operation(op)
                    op.reset()
                    neighbor.schedule(op, machine)

                    # Évaluer le voisin
                    neighbor_value = neighbor.evaluate
                    if neighbor_value <= best_value:
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
                    neighbor = copy.deepcopy(sol)
                    op = next(op for op in neighbor.all_operations if op.operation_id == operation.operation_id)
                    # Retirer l'opération de la machine d'origine dans la copie
                    current_machine = next((m for m in neighbor.inst.machines if m.machine_id == current_machine_id), None)
                    if current_machine is not None:
                        current_machine.remove_operation(op)
                    op.reset()
                    neighbor.schedule(op, machine)

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
                    neighbor = _create_neighbor_solution(sol, machine_ops[i], machine_ops[j], machine)

                    # Vérifie la faisabilité avant de retourner
                    if neighbor.is_feasible and neighbor.evaluate < current_value:
                        return neighbor

        return sol


def _create_neighbor_solution(sol: Solution, op1, op2, machine):
    '''
    Helper function to create a neighbor solution by swapping two operations.
    '''
    neighbor = copy.deepcopy(sol)


    machine.remove_operation(op1)
    machine.remove_operation(op2)

    op1.reset()
    op2.reset()

    # S'assurer qu'elles ne sont pas dans d'autres listes
    if hasattr(neighbor, "scheduled_operations"):
        if op1 in neighbor.scheduled_operations:
            neighbor.scheduled_operations.remove(op1)
        if op2 in neighbor.scheduled_operations:
            neighbor.scheduled_operations.remove(op2)

    # Les ajouter à available_operations
    if op1 not in neighbor.available_operations:
        neighbor.available_operations.append(op1)
    if op2 not in neighbor.available_operations:
        neighbor.available_operations.append(op2)

    # Réassigner dans l'ordre inverse
    neighbor.schedule(op2, machine)
    neighbor.schedule(op1, machine)

    return neighbor
