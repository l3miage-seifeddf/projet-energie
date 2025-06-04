'''
Object containing the solution to the optimization problem.

@author: Vassilissa Lehoux
'''
from typing import List
from matplotlib import pyplot as plt

from src.scheduling.instance.machine import Machine
from src.scheduling.instance.instance import Instance
from src.scheduling.instance.operation import Operation

from matplotlib import colormaps
from src.scheduling.instance.machine import Machine


class Solution(object):
    '''
    Solution class
    '''

    def __init__(self, instance: Instance):
        '''
        Constructor
        '''
        self._instance = instance
        self._operations = {op: None for op in instance.operations}


    @property
    def inst(self):
        '''
        Returns the associated instance
        '''
        return self._instance


    def reset(self):
        '''
        Resets the solution: everything needs to be replanned
        '''
        self._operations = {op: None for op in self._instance.operations}

    @property
    def is_feasible(self) -> bool:
        '''
        Returns True if the solution respects the constraints.
        To call this function, all the operations must be planned.
        '''
        return all(op.assigned for op in self._operations.keys())

    @property
    def evaluate(self) -> int:
        '''
        Computes the value of the solution
        '''
        return self.objective

    @property
    def objective(self) -> int:
        '''
        Returns the value of the objective function
        '''
        return self.total_energy_consumption + self.cmax

    @property
    def cmax(self) -> int:
        '''
        Returns the maximum completion time of a job
        '''
        return max(op.end_time for op in self._operations.keys())

    @property
    def sum_ci(self) -> int:
        '''
        Returns the sum of completion times of all the jobs
        '''
        return sum(op.end_time for op in self._operations.keys())

    @property
    def total_energy_consumption(self) -> int:
        '''
        Returns the total energy consumption for processing
        all the jobs (including energy for machine switched on but doing nothing).
        '''
        return sum(machine.total_energy_consumption for machine in self._instance.machines)

    def __str__(self) -> str:
        '''
        String representation of the solution
        '''
        return ""

    def to_csv(self):
        '''
        Save the solution to a csv files with the following formats:
        Operation file:
          One line per operation
          operation id - machine to which it is assigned - start time
          header: "operation_id,machine_id,start_time"
        Machine file:
          One line per pair of (start time, stop time) for the machine
          header: "machine_id, start_time, stop_time"
        '''
        raise "Not implemented error"

    def from_csv(self, inst_folder, operation_file, machine_file):
        '''
        Reads a solution from the instance folder
        '''
        raise "Not implemented error"

    @property
    def available_operations(self)-> List[Operation]:
        '''
        Returns the available operations for scheduling:
        all constraints have been met for those operations to start
        '''
        return [
            op for op in self._operations.keys()
            if op.is_ready(min(machine.available_time for machine in self._instance.machines))
        ]
    @property
    def all_operations(self) -> List[Operation]:
        '''
        Returns all the operations in the instance
        '''
        return list(self._operations.keys())

    def schedule(self, operation: Operation, machine: Machine):
        '''
        Schedules the operation at the end of the planning of the machine.
        Starts the machine if stopped.
        @param operation: an operation that is available for scheduling
        '''
        assert(operation in self.available_operations)
        start_time = max(machine.available_time, operation.min_start_time)
        machine.add_operation(operation, start_time)

    def gantt(self, colormapname):
        """
        Generate a plot of the planning.
        Standard colormaps can be found at https://matplotlib.org/stable/users/explain/colors/colormaps.html
        """
        fig, ax = plt.subplots()
        colormap = colormaps[colormapname]
        for machine in self.inst.machines:
            machine_operations = sorted(machine.scheduled_operations, key=lambda op: op.start_time)
            for operation in machine_operations:
                operation_start = operation.start_time
                operation_end = operation.end_time
                operation_duration = operation_end - operation_start
                operation_label = f"O{operation.operation_id}_J{operation.job_id}"
    
                # Set color based on job ID
                color_index = operation.job_id + 2
                if color_index >= colormap.N:
                    color_index = color_index % colormap.N
                color = colormap(color_index)
    
                ax.broken_barh(
                    [(operation_start, operation_duration)],
                    (machine.machine_id - 0.4, 0.8),
                    facecolors=color,
                    edgecolor='black'
                )

                middle_of_operation = operation_start + operation_duration / 2
                ax.text(
                    middle_of_operation,
                    machine.machine_id,
                    operation_label,
                    rotation=90,
                    ha='center',
                    va='center',
                    fontsize=8
                )
            set_up_time = machine.set_up_time
            tear_down_time = machine.tear_down_time
            for (start, stop) in zip(machine.start_times, machine.stop_times):
                start_label = "set up"
                stop_label = "tear down"
                ax.broken_barh(
                    [(start, set_up_time)],
                    (machine.machine_id - 0.4, 0.8),
                    facecolors=colormap(0),
                    edgecolor='black'
                )
                ax.broken_barh(
                    [(stop, tear_down_time)],
                    (machine.machine_id - 0.4, 0.8),
                    facecolors=colormap(1),
                    edgecolor='black'
                )
                ax.text(
                    start + set_up_time / 2.0,
                    machine.machine_id,
                    start_label,
                    rotation=90,
                    ha='center',
                    va='center',
                    fontsize=8
                )
                ax.text(
                    stop + tear_down_time / 2.0,
                    machine.machine_id,
                    stop_label,
                    rotation=90,
                    ha='center',
                    va='center',
                    fontsize=8
                )          

        fig = ax.figure
        fig.set_size_inches(12, 6)
    
        ax.set_yticks(range(self._instance.nb_machines))
        ax.set_yticklabels([f'M{machine_id+1}' for machine_id in range(self.inst.nb_machines)])
        ax.set_xlabel('Time')
        ax.set_ylabel('Machine')
        ax.set_title('Gantt Chart')
        ax.grid(True)
    
        return plt
