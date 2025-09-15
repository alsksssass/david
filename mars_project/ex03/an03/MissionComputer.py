import DummySensor
import json
import time
import os
import platform
import psutil


class MissonComputer:
    def __init__(self):
        self.ds = DummySensor.DummySensor()
        self.os = platform.system()
        self.os_version = platform.version()
        self.cpu_actucture = platform.machine()
        self.cpu_cores = os.cpu_count()

    def to_json(self, data):
        return json.dumps(data, ensure_ascii=False, indent="\t")

    def get_sensor_data(self):
        try:
            while True:
                self.ds.set_env()
                print(self.to_json(self.ds.get_env()))
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nThe computer is shutdown")
            os._exit(0)
        except Exception as e:
            print(f"error : {e}")

    def get_misson_computer_info(self):
        data = {
            "OS:": self.os,
            "OS version:": self.os_version,
            "Machine:": self.cpu_actucture,
            "CPU cores (logical):": self.cpu_cores,
        }
        print(self.to_json(data))

    def get_mission_computer_load(self):
        data = {
            "CPU usage": f"{psutil.cpu_percent(interval=1)}%",
            "Memory usage": f"{psutil.virtual_memory().percent}%",
        }
        print(self.to_json(data))
