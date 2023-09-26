import multiprocessing
import threading

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
        self.stop_event = multiprocessing.Event()
        self.status = dict()

    @threaded
    def execute_scripts(self):
        for script in self.task.scripts:
            if self.stop_event.is_set():
                self.status[script.db_id] = TaskStatus.CANCELLED
                break
            try:
                executor = ExecutorFactory.create_executor(script.db_id, **script.kwargs)
                self.process = multiprocessing.Process(target=executor.run, args=(self.stop_event,))
                self.process.start()
                self.process.join()
                self.status[script.db_id] = TaskStatus.COMPLETED\
                    if self.process.exitcode == TaskStatus.COMPLETED\
                    else TaskStatus.FAILED
            except Exception as e:
                print(f'Failed to execute script: {e}')
                self.status[script.db_id] = TaskStatus.FAILED

        self.task.set_scripts_status(self.status)
        self.task.set_status(TaskStatus.COMPLETED if all(self.status.values()) else TaskStatus.FAILED)

    def get_scripts_status(self):
        pass
