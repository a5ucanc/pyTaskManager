from abc import ABC, abstractmethod


class ExecutorAPI(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def help(self):
        if self.__doc__ is None:
            return "No help available for this executor."

        return self.__doc__

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def status(self):
        pass
