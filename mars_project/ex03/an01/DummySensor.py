import random
import json
import pprint


class DummySensor:
    def __init__(self):
        self.mars_base_internal_temperature = 0
        self.mars_base_external_temperature = 0
        self.mars_base_internal_humidity = 0
        self.mars_base_external_illuminance = 0
        self.mars_base_internal_co2 = 0
        self.mars_base_internal_oxygen = 0

    def set_env(self):
        self.mars_base_internal_temperature = random.randint(18, 30)
        self.mars_base_external_temperature = random.randint(0, 21)
        self.mars_base_internal_humidity = random.randint(50, 60)
        self.mars_base_external_illuminance = random.randint(500, 715)
        self.mars_base_internal_co2 = round(random.uniform(0.02, 0.1), 3)
        self.mars_base_internal_oxygen = random.randint(4, 7)

    def get_env(self):
        return {
            "internal_temperature": self.mars_base_internal_temperature,
            "external_temperature": self.mars_base_external_temperature,
            "internal_humidity": self.mars_base_internal_humidity,
            "external_illuminance": self.mars_base_external_illuminance,
            "internal_co2": self.mars_base_internal_co2,
            "internal_oxygen": self.mars_base_internal_oxygen,
        }
