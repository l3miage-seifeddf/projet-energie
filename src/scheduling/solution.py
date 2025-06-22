'''
Object containing the solution to the optimization problem.

@author: Vassilissa Lehoux
'''
import csv
import math
import os
import sys
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
        return all(op.assigned for op in self.all_operations)

    @property
    def evaluate(self) -> int:
        '''
        Computes the value of the solution
        If the solution is not feasible, returns infinity as int
        '''
        if not self.is_feasible:
            return sys.maxsize
        return self.objective

    @property
    def objective(self) -> int:
        '''
        Returns the value of the objective function
        thos obective function is total of energy consumption, the time at whitch the last job is completed and
        la moyenne de durée des tâcches
        '''
        return self.total_energy_consumption + self.cmax + self.mean_processing_time()

    def mean_processing_time(self) -> int:
        '''
        Returns the mean processing time of all the jobs
        operations are included in a Job so we need the mean processing time of jobs considering
        the difference between the end_time of the last operation and the start_time of the first operation

        return the result as an integer
        '''

        total_processing_time = sum(op.end_time - op.start_time for op in self._operations.keys() if op.assigned)
        total_jobs = len(self._instance.jobs)
        if total_jobs == 0:
            return 0
        return total_processing_time // total_jobs if total_jobs > 0 else 0


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

    def to_csv(self, folder_path="output"):
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
        os.makedirs(folder_path, exist_ok=True)
        op_file = os.path.join(folder_path, "operations.csv")
        machine_file = os.path.join(folder_path, "machines.csv")

        # Fichier des opérations
        with open(op_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["operation_id", "machine_id", "start_time"])
            for op in self.all_operations:
                if op.assigned:
                    writer.writerow([op.operation_id, op.assigned_to, op.start_time])

        # Fichier des machines
        with open(machine_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["machine_id", "start_time", "stop_time"])
            for machine in self.inst.machines:
                for start, stop in zip(machine.start_times, machine.stop_times):
                    writer.writerow([machine.machine_id, start, stop])

    def from_csv(self, inst_folder, operation_file, machine_file):
        '''
        Reads a solution from the instance folder
        '''
        # Réinitialise la solution
        self.reset()

        # Restaure les périodes d'allumage des machines
        machine_path = os.path.join(inst_folder, machine_file)
        with open(machine_path, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                machine_id = int(row["machine_id"])
                start = int(row["start_time"])
                stop = int(row["stop_time"])
                machine = next(m for m in self._instance.machines if m.machine_id == machine_id)
                machine.start_times.append(start)
                machine.stop_times.append(stop)

        # Restaure les opérations planifiées
        op_path = os.path.join(inst_folder, operation_file)
        with open(op_path, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                op_id = int(row["operation_id"])
                machine_id = int(row["machine_id"])
                start_time = int(row["start_time"])
                op = next(o for o in self.all_operations if o.operation_id == op_id)
                machine = next(m for m in self._instance.machines if m.machine_id == machine_id)
                machine.add_operation(op, start_time)

    @property
    def available_operations(self)-> List[Operation]:
        '''
        Returns the available operations for scheduling:
        all constraints have been met for those operations to start
        '''
        available = []
        for job in self._instance.jobs:
            for idx, op in enumerate(job.operations):
                if op.assigned:
                    continue
                if idx == 0:
                    available.append(op)
                else:
                    prev_op = job.operations[idx - 1]
                    if prev_op.assigned and prev_op.end_time <= max(m.available_time for m in self._instance.machines):
                        available.append(op)
        return available


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
        assert (operation in self.available_operations)

        start_time = max(machine.available_time, operation.min_start_time)
        if not machine.is_on(start_time):
            start_up_time = max(0, operation.min_start_time - machine.set_up_time)
            machine.start(start_up_time)
            start_time = max(machine.available_time, start_up_time + machine.set_up_time)
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
