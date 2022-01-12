from logic.environment.simulation_objects import Thermometer, HumiditySensor, Barometer, get_time, PressureParams, TemperatureParams, HumidityParams
from logic.communication.receiver import Receiver
from logic.communication.sender import Sender
from logic.communication.constants import *
from threading import Thread
from logic.environment.simulation_objects import get_time
import random
import datetime
import json
from time import sleep


def time_now():
    t_now = datetime.datetime.now()
    time = t_now.hour + t_now.minute / 60
    return get_time() # get_time() to funkcja symulacji
    # return time


class Room:
    def __init__(self, thermometer: Thermometer, humidity_sensor: HumiditySensor, barometer: Barometer,
                 receiver: Receiver, sender: Sender, temperature_delta=0.2, humidity_delta=0.05):
        self.thermometer = thermometer
        self.humidity_sensor = humidity_sensor
        self.barometer = barometer
        self.is_thermostat_on = False
        self.is_dryer_on = False
        self.current_temperature = thermometer.current_temperature(get_time())
        self.current_humidity = humidity_sensor.current_humidity(get_time())
        self.receiver = receiver
        self.sender = sender
        self.temperature_delta = temperature_delta
        self.humidity_delta = humidity_delta
        self.last_measurement = time_now()

        with open('config.json') as file:
            config = json.load(file)
            self.name = config['name']

        self.last_sent = time_now()

    def update_temperature(self):
        time = time_now()
        temp = self.thermometer.current_temperature(time)
        temp_change = 0.0

        if self.is_thermostat_on:
            temp_change = (self.temperature_delta * random.random())
        elif self.current_temperature < temp:
            temp_change = (self.temperature_delta * random.random())
        else:
            temp_change -= (self.temperature_delta * random.random())

        self.current_temperature += temp_change

    def update_humidity(self):
        time = time_now()
        humidity = self.humidity_sensor.current_humidity(time)
        humidity_change = 0

        if self.is_dryer_on:
            humidity_change -= (self.humidity_delta * random.random())
        elif self.current_humidity < humidity:
            humidity_change += (self.humidity_delta * random.random())
        else:
            humidity -= (self.humidity_delta * random.random())

        self.current_humidity += min(max(humidity_change, 0), 1)

    def update_devices(self, message):
        name, is_thermostat_on, is_dryer_on = self.__decode_message(message.payload.decode('utf-8'))
        if name.upper() == self.name.upper():
            self.is_dryer_on = is_dryer_on
            self.is_thermostat_on = is_thermostat_on
            print(f'device updated:\nThermostat on: {self.is_thermostat_on}\nDryer on: {self.is_dryer_on}\n')

    def __decode_message(self, message: str):
        name, thermostat, dryer = message.split('#')
        is_thermostat_on = True if thermostat.upper() == 'TRUE' else False
        is_dryer_on = True if dryer.upper() == 'TRUE' else False
        return name, is_thermostat_on, is_dryer_on

    def listening(self):
        self.receiver.connect_to_broker()
        self.receiver.loop_start()
        self.receiver.client.on_message = lambda client, userdata, message: self.update_devices(message)
        self.receiver.subscribe()
        while True:
            pass

    def sending(self):
        self.sender.connect_to_broker()
        while True:
            t_now = time_now()
            # time_now = datetime.datetime.now()
            if t_now - self.last_sent > 0.02:
                temp = round(self.thermometer.current_temperature(t_now), 3)
                hum = round(self.humidity_sensor.current_humidity(t_now), 2)
                pres = round(self.barometer.current_pressure(t_now), 2)
                self.sender.publish(f"{self.name}#{temp}#{hum}#{pres}")
                self.last_sent = t_now


def main():
    tempParams = TemperatureParams(10, 17, 0.3)
    humParams = HumidityParams(0, 0.78, 0.01, tempParams)
    presParams = PressureParams(970, 1020, 1)
    therm = Thermometer(tempParams)
    humSensor = HumiditySensor(humParams)
    barom = Barometer(presParams)
    sender = Sender('localhost', ROOM_DATA)  # ip do zmiany
    receiver = Receiver('localhost', DIRECTIVES)  # ip do zmiany
    room = Room(therm, humSensor, barom, receiver, sender, temperature_delta=0.07, humidity_delta=0.02)
    Thread(target=lambda: room.listening()).start()
    Thread(target=lambda: room.sending()).start()
    while True:
        pass


if __name__ == '__main__':
    main()





