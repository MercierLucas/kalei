from typing import Dict, List, Callable
from enum import Enum


class Events(Enum):
    # UPDATES
    ON_CAMERA_UPDATED=0
    ON_OBJECTS_UPDATE=1
    ON_OBJECT_SELECTED=2
    ON_OBJECT_ADDED_TO_SCENE=3
    ON_ADD_SAMPLE_OBJECT=4

    # KEYS-RELATED
    ON_MOVE_CAMERA=20

    # DRAW
    ON_SCENE_READY_TO_DRAW=30


class EventManager:
    def __init__(self) -> None:
        self.listerners:Dict[Events, List[Callable]] = {}
    

    def register(self, event_name:Events, func:Callable):
        if event_name not in self.listerners:
            self.listerners[event_name] = []
        if func not in self.listerners[event_name]:
            self.listerners[event_name].append(func)

    
    def trigger(self, event_name:Events, *args, **kwargs):
        # assert event_name in self.listerners, f"Not registered event called {event_name}"
        if event_name not in self.listerners:
            return

        for func in self.listerners[event_name]:
            func(*args, **kwargs)


event_manager = EventManager()