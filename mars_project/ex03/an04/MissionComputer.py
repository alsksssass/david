import DummySensor
import json
import time
import os
import platform
import psutil


class MissonComputer:
    def __init__(self):
        self.ds = DummySensor.DummySensor() or "sensor Error"
        self.os = platform.system() or "system info Error"
        self.os_version = platform.version() or "system version Error"
        self.cpu_actucture = platform.machine() or "actucture info Error"
        self.cpu_cores = os.cpu_count() or "cpu core Error"

    def to_json(self, data):
        return json.dumps(data, ensure_ascii=False, indent="\t")

    def get_sensor_data(self, lock, event=None):
        try:
            while True:
                self.ds.set_env()
                with lock:
                    print("===== sensor data info =====")
                    print(self.to_json(self.ds.get_env()))
                if event is None:
                    time.sleep(5)
                else:
                    event.wait(5)
                    if event.is_set():
                        break
        except KeyboardInterrupt:
            print("\nThe computer is shutdown")
        except Exception as e:
            print(f"error : {e}")

    def get_misson_computer_info(self, lock, event=None):
        data = {
            "OS:": self.os or "os info Error",
            "OS version:": self.os_version or "os version Error",
            "Machine:": self.cpu_actucture or "cpu actucure Error",
            "CPU cores (logical):": self.cpu_cores or "cpu core Error",
        }
        try:
            while True:
                with lock:
                    print("===== mission computer info =====")
                    print(self.to_json(data))
                if event is None:
                    time.sleep(20)
                else:
                    event.wait(20)
                    if event.is_set():
                        break
        except KeyboardInterrupt:
            print("\nThe computer is shutdown")
        except Exception as e:
            print(f"error : {e}")

    def get_mission_computer_load(self, lock, event=None):
        psutil.cpu_percent(interval=None)
        try:
            while True:
                data = {
                    "CPU usage": f"{psutil.cpu_percent(interval=None)}%",
                    "Memory usage": f"{psutil.virtual_memory().percent}%",
                }
                with lock:
                    print("===== mission computer usage =====")
                    print(self.to_json(data))
                if event is None:
                    time.sleep(20)
                else:
                    event.wait(20)
                    if event.is_set():
                        break
        except KeyboardInterrupt:
            print("\nThe computer is shutdown")
        except Exception as e:
            print(f"error : {e}")
