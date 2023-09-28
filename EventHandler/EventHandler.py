import multiprocessing
import threading
from collections.abc import Callable
from enum import Enum


class EventTypes(Enum):
    STATUS_EVENT = 'status_event'
    STOP_EVENT = 'stop_event'
    PAUSE_EVENT = 'pause_event'
    RESUME_EVENT = 'resume_event'


class HandlerThread:
    def __init__(self, event, callback):
        self.event = event
        self.callback = callback
        self.terminate = threading.Event()
        self.thread = None

    def start_handler(self):
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
        self.events: dict[multiprocessing.Event, Callable] = dict()
        self.event_names = dict()
        self.listeners: list[HandlerThread] = list()
        self.queue = multiprocessing.Queue()

    def start_handlers(self):
        for event, callback in self.events.items():
            ht = HandlerThread(event, callback)
            ht.start_handler()
            self.listeners.append(ht)

    def stop_handlers(self):
        if self.listeners:
            for listener in self.listeners:
                listener.stop_handler()

    def register_event(self, event_name: str, event: multiprocessing.Event, callback: Callable):
        self.events[event] = callback
        self.event_names[event_name] = event
