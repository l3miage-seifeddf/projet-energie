'''
Information for the instance of the optimization problem.

@author: Vassilissa Lehoux
'''
import csv
import os
from typing import List

from src.scheduling.instance.job import Job
from src.scheduling.instance.machine import Machine
from src.scheduling.instance.operation import Operation


class Instance(object):
    '''
    classdocs
    '''

    def __init__(self, instance_name):
        self._instance_name = instance_name
        self._jobs = []
        self._machines = []
        self._operations = []

    @classmethod
    def from_file(cls, folderpath):
        inst = cls(os.path.basename(folderpath))
        # Reading the operation inf
        seen_operations = set()
        with open(folderpath + os.path.sep + inst._instance_name + '_op.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                job_id = int(row[0])
                operation_id = int(row[1])
                key = (job_id, operation_id)
                if key not in seen_operations:
                    operation = Operation(job_id, operation_id)
                    inst._operations.append(operation)
                    operation.processing_times[int(row[2])] = int(row[3])
                    operation.energies[int(row[2])] = int(row[4])
                    seen_operations.add(key)
                else:
                    # If the operation already axists, add the processing time and energy for the machine
                    operation = inst.get_operation(operation_id)
                    operation.processing_times[int(row[2])] = int(row[3])
                    operation.energies[int(row[2])] = int(row[4])




        # reading machine info
        with open(folderpath + os.path.sep + inst._instance_name + '_mach.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                machine_id = int(row[0])
                set_up_time = int(row[1])
                set_up_energy = int(row[2])
                tear_down_time = int(row[3])
                tear_down_energy = int(row[4])
                min_consumption = int(row[5])
                end_time = int(row[6])
                machine = Machine(machine_id, set_up_time, set_up_energy, tear_down_time,
                                  tear_down_energy, min_consumption, end_time)
                inst._machines.append(machine)

        for operation in inst._operations:
            job_id = operation.job_id
            while len(inst._jobs) <= job_id:
                inst._jobs.append(Job(job_id))
            inst._jobs[job_id].add_operation(operation)
        return inst

    @property
    def name(self):
        return self._instance_name

    @property
    def machines(self) -> List[Machine]:
        return self._machines

    @property
    def jobs(self) -> List[Job]:
        return self._jobs

    @property
    def operations(self) -> List[Operation]:
        return self._operations

    @property
    def nb_jobs(self):
        return len(self._jobs)

    @property
    def nb_machines(self):
        return len(self._machines)

    @property
    def nb_operations(self):
        return len(self._operations)

    def __str__(self):
        return f"{self.name}_M{self.nb_machines}_J{self.nb_jobs}_O{self.nb_operations}"

    def get_machine(self, machine_id) -> Machine:
        return next((machine for machine in self._machines if machine.machine_id == machine_id), None)

    def get_job(self, job_id) -> Job:
        return next((job for job in self._jobs if job.job_id == job_id), None)

    def get_operation(self, operation_id) -> Operation:
        return next((op for op in self._operations if op.operation_id == operation_id), None)
