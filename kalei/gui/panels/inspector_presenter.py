from .inspector_ui import InspectorPanel

from kalei.events import event_manager, Events
from kalei.engine import Object



class InspectorPresenter:
    def __init__(self, config:dict, pos_x:int, pos_y:int) -> None:
        self.panel = InspectorPanel(config)
        self.panel.init_ui(pos_x, pos_y)

        event_manager.register(Events.ON_OBJECT_SELECTED, self.object_selected)

    
    def object_selected(self, obj:Object):
        self.panel.object_selected(obj)



