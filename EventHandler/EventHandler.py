import multiprocessing
import threading
from collections.abc import Callable
from enum import Enum


class EventTypes(Enum):
    STATUS_EVENT = 'status_event'
    TERMINATE_EVENT = 'terminate_event'
    PAUSE_EVENT = 'pause_event'


class HandlerThread:
    def __init__(self, event_name, event, callback):
        self.event_name = event_name
        self.event = event
        self.callback = callback
        self.terminate = threading.Event()
        self.thread = threading.Thread(target=self.handler)
        self.thread.start()

    def handler(self):
        while not self.terminate.is_set():
            if self.event.wait(timeout=1):
                self.callback()
                self.event.clear()

    def stop_handler(self):
        self.terminate.set()


class EventHandler:
    def __init__(self):
        self.events: dict[str, multiprocessing.Event] = dict()
        self.listeners: list[HandlerThread] = list()

    def start_handlers(self, mapping: dict[str, Callable]):
        for event_name, event in self.events.items():
            self.listeners.append(HandlerThread(event_name, event, mapping[event_name]))

    def stop_handlers(self):
        if self.listeners:
            for listener in self.listeners:
                listener.stop_handler()

    def add_event(self, event_name: str, callback: Callable):
        self.events[event_name] = callback
