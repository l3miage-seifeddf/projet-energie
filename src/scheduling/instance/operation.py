'''
Operation of a job.
Its duration and energy consumption depends on the machine on which it is executed.
When operation is scheduled, its schedule information is updated.

@author: Vassilissa Lehoux
'''
from typing import List


class OperationScheduleInfo(object):
    '''
    Informations known when the operation is scheduled
    '''

    def __init__(self, machine_id: int, schedule_time: int, duration: int, energy_consumption: int):
        self.machine_id = machine_id
        self.schedule_time = schedule_time
        self.duration = duration
        self.energy_consumption = energy_consumption


class Operation(object):
    '''
    Operation of the jobs
    '''

    def __init__(self, job_id, operation_id):
        '''
        Constructor
        '''
        self._job_id = job_id
        self._operation_id = operation_id
        self._schedule_info = None
        self._predecessors = []
        self._successors = []
        self.energies = {}
        self.processing_times = {}


    def __str__(self):
        '''
        Returns a string representing the operation.
        '''
        base_str = f"O{self.operation_id}_J{self.job_id}"
        if self._schedule_info:
            return base_str + f"_M{self.assigned_to}_ci{self.processing_time}_e{self.energy}"
        else:
            return base_str

    def __repr__(self):
        return str(self)

    def reset(self):
        '''
        Removes scheduling informations
        '''
        self._schedule_info = None

    def add_predecessor(self, operation):
        '''
        Adds a predecessor to the operation
        '''
        self._predecessors.append(operation)

    def add_successor(self, operation):
        '''
        Adds a successor operation
        '''
        self._successors.append(operation)

    @property
    def operation_id(self) -> int:
        return self._operation_id

    @property
    def job_id(self) -> int:
        return self._job_id
    @property
    def predecessors(self) -> List:
        """
        Returns a list of the predecessor operations
        """
        return self._predecessors

    @property
    def successors(self) -> List:
        '''
        Returns a list of the successor operations
        '''
        return self._successors

    @property
    def assigned(self) -> bool:
        '''
        Returns True if the operation is assigned
        and False otherwise
        '''
        return self._schedule_info is not None

    @property
    def assigned_to(self) -> int:
        '''
        Returns the machine ID it is assigned to if any
        and -1 otherwise
        '''
        return self._schedule_info.machine_id if self.assigned else -1


    @property
    def processing_time(self) -> int:
        '''
        Returns the processing time if is assigned,
        -1 otherwise
        '''
        return self._schedule_info.duration if self.assigned else -1

    @property
    def start_time(self) -> int:
        '''
        Returns the start time if is assigned,
        -1 otherwise
        '''
        return self._schedule_info.schedule_time if self.assigned else -1

    @property
    def end_time(self) -> int:
        '''
        Returns the end time if is assigned,
        -1 otherwise
        '''
        return self._schedule_info.schedule_time + self.processing_time if self.assigned else -1

    @property
    def energy(self) -> int:
        '''
        Returns the energy consumption if is assigned,
        -1 otherwise
        '''
        return self._schedule_info.energy_consumption if self.assigned else -1

    def is_ready(self, at_time) -> bool:
        '''
        Returns True if all the predecessors are assigned
        and processed before at_time.
        False otherwise
        '''
        return all((0 <= pred.end_time <= at_time) for pred in self._predecessors)

    def schedule(self, machine_id: int, at_time: int, check_success=True) -> bool:
        '''
        Schedules an operation. Updates the schedule information of the operation
        @param check_success: if True, check if all the preceeding operations have
          been scheduled and if the schedule time is compatible
        '''
        if check_success and not self.is_ready(at_time):
            return False
        self._schedule_info = OperationScheduleInfo(machine_id, at_time, self.processing_times[machine_id], self.energies[machine_id])
        return True

    @property
    def min_start_time(self) -> int:
        '''
        Minimum start time given the precedence constraints
        '''
        return max(pred.end_time for pred in self._predecessors) if self._predecessors else 0

    def schedule_at_min_time(self, machine_id: int, min_time: int) -> bool:
        '''
        Try and schedule the operation af or after min_time.
        Return False if not possible
        '''
        self.schedule(machine_id, min_time, False)
