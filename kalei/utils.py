import time
import yaml


class FPSCounter:
    def __init__(self) -> None:
        self.last_time = time.time()
    
    def tick(self) -> float:
        curr_time = time.time()
        ellasped = curr_time - self.last_time
        try:
            fps = 1 / ellasped
        except ZeroDivisionError:
            fps = 0
        self.last_time = curr_time
        return fps, ellasped



def load_config(path:str=None) -> dict:
    if path is None:
        path = "configs/global.yaml"
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            return None




if __name__ == "__main__":
    print(load_config())