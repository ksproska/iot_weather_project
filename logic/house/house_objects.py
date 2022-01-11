from logic.environment.simulation_objects import Thermometer, HumiditySensor, get_time


class Room:
    def __init__(self, idx: int, thermometer: Thermometer, humidity_sensor: HumiditySensor, name=""):
        self.id = idx
        self.thermometer = thermometer
        self.humidity_sensor = humidity_sensor
        self.name = name
        self.is_thermostat_on = False
        self.is_dryer_on = False
        self.current_temperature = thermometer.current_temperature(get_time())
        self.current_humidity = humidity_sensor.current_humidity(get_time())


