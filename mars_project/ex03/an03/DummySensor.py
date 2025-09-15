import random


class DummySensor:
    def __init__(self):
        self.dic = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0,
        }

    def set_env(self):
        self.dic["mars_base_internal_temperature"] = random.randint(18, 30)
        self.dic["mars_base_external_temperature"] = random.randint(0, 21)
        self.dic["mars_base_internal_humidity"] = random.randint(50, 60)
        self.dic["mars_base_external_illuminance"] = random.randint(500, 715)
        self.dic["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.dic["mars_base_internal_oxygen"] = random.randint(4, 7)

    def get_env(self):
        return self.dic
