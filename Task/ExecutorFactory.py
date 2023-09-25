from dataclasses import dataclass
import importlib

from API.ExecutorAPI import ExecutorAPI


@dataclass
class Executor:
    id: int
    path: str


def static_class(cls):
    return cls()


@static_class
class ExecutorFactory:
    EXECUTOR = {}

    @classmethod
    def register_executor(cls, executor: Executor) -> None:
        script_module = importlib.import_module(executor.path)
        try:
            executor_class = getattr(script_module, 'ToolExecutor')
        except AttributeError:
            raise Exception(f"Executor {executor.path} does not contain ToolExecutor class")

        if not isinstance(executor_class, type) and issubclass(executor_class, ExecutorAPI):
            raise Exception(f"Executor {executor_class} is not a subclass of ExecutorAPI")

        cls.EXECUTOR[executor.id] = executor_class

    @classmethod
    def create_executor(cls, executor_id, **kwargs) -> ExecutorAPI:
        return cls.EXECUTOR[executor_id](**kwargs)
