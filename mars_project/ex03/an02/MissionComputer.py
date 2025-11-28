import DummySensor
import json
import time
import os


class MissonComputer:
    def __init__(self):
        self.ds = DummySensor.DummySensor()

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
