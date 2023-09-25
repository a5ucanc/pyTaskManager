from datetime import datetime

from API.constants import TaskStatus
from ExecutorFactory import ExecutorFactory


class Executor:
    def __init__(self, db_id: int, **kwargs):
        self.db_id = db_id
        self.kwargs = kwargs


class ScheduleConfig:
    def __init__(self, start: datetime, end: datetime, repeat_interval: datetime):
        self.start = start
        self.end = end
        self.repeat_interval = repeat_interval


class Task:
    def __int__(self, name: str, description: str, schedule: ScheduleConfig | None,
                executors: Executor | list[Executor], run_immediately: bool = False):
        self.name = name
        self.description = description
        self.schedule = schedule
        self.executors = executors
        self.run_immediately = run_immediately
        self.status = TaskStatus.NOT_STARTED

    def start(self):
        if type(self.executors, list):
            status = dict()
            for executor in self.executors:
                executor_obj = ExecutorFactory.create_executor(executor.db_id, **executor.kwargs)
                return_status = executor_obj.run()
                status[executor.db_id] = return_status
        else:
            executor_obj = ExecutorFactory.create_executor(self.executors.db_id, **self.executors.kwargs)
            status = executor_obj.run()

        return status
