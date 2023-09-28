import multiprocessing
import threading

from EventHandler.EventHandler import EventHandler, EventTypes
from Task.ExecutorFactory import ExecutorFactory
from Task.Task import TaskStatus


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class TaskExecutor:
    def __init__(self, task):
        self.task = task
        self.process = None
        self.execution_status = dict()
        self.event_handler = EventHandler()

    @threaded
    def execute_scripts(self):
        stop_event = self.event_handler.event_names[EventTypes.STOP_EVENT]
        for script in self.task.scripts:
            if stop_event.is_set():
                self.execution_status[script.id] = TaskStatus.CANCELLED
                break

            executor = ExecutorFactory.create_executor(script.id, **script.kwargs)
            self.process = multiprocessing.Process(target=executor.run, args=())
            self.process.start()
            self.execution_status[script.id] = TaskStatus.IN_PROGRESS
            self.process.join()
            if self.process.exitcode == TaskStatus.COMPLETED:
                self.execution_status[script.id] = TaskStatus.COMPLETED
            else:
                self.execution_status[script.id] = TaskStatus.FAILED

        self.task.set_scripts_status(self.execution_status)
        self.task.set_status(TaskStatus.COMPLETED if all(self.execution_status.values()) else TaskStatus.FAILED)

    def stop(self):
        self.event_handler.event_names[EventTypes.STOP_EVENT].set()

    def get_execution_status(self):
        status = self.execution_status
        self.event_handler.event_names[EventTypes.STATUS_EVENT].set()
        last_process = set(self.execution_status.keys()).pop()
        status[last_process] = self.event_handler.queue.get(timeout=1)
        return status
