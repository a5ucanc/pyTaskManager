from datetime import datetime
from enum import Enum

from Task.TaskExecutor import TaskExecutor


class TaskStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    CANCELLED = 4


class Script:
    def __init__(self, id: int, **kwargs):
        self.id = id
        self.kwargs = kwargs


class ScheduleConfig:
    def __init__(self, start: datetime, end: datetime, repeat_interval: datetime):
        self.start = start
        self.end = end
        self.repeat_interval = repeat_interval


class Task:
    def __init__(self, name: str, description: str, schedule: ScheduleConfig | None,
                 scripts: Script | list[Script], run_immediately: bool = False):
        if isinstance(scripts, Script):
            scripts = [scripts]
        self.scripts = scripts
        self.name = name
        self.description = description
        self.schedule = schedule
        self.run_immediately = run_immediately
        self.status = TaskStatus.NOT_STARTED
        self.scripts_status = dict()
        self.task_executor = None

    def start(self):
        if self.status != TaskStatus.IN_PROGRESS:
            self.task_executor = TaskExecutor(self)
            self.task_executor.execute_scripts()
            self.status = TaskStatus.IN_PROGRESS

    def set_status(self, status: TaskStatus):
        self.status = status

    def set_scripts_status(self, scripts_status: dict[int, TaskStatus]):
        self.scripts_status = scripts_status

    def get_execution_status(self):
        if self.status == TaskStatus.IN_PROGRESS:
            return self.task_executor.get_scripts_status()
        return self.scripts_status
