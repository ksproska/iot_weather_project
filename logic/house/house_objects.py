import sys
# sys.path.append('path')
SERVER_IP = '25.33.38.163'
from logic.environment.simulation_objects import Thermometer, HumiditySensor, Barometer, PressureParams, TemperatureParams, HumidityParams
from logic.communication.receiver import Receiver
from logic.communication.sender import Sender
from logic.communication.constants import *
from threading import Thread
from logic.environment.simulation_objects import simulated_time, normal_time
import random
import datetime
import json
from time import sleep


def time_now(month=1):
    return normal_time()
    # return simulated_time(month=month)


class Room:
    MINUTE_5 = 0.08
    MINUTE_2 = 0.032
    MINUTE_1 = 0.016
    SECONDS_30 = 0.008
    SECONDS_15 = 0.004
    SECONDS_5 = 0.0013

    def __init__(self, thermometer: Thermometer, humidity_sensor: HumiditySensor, barometer: Barometer,
                 receiver: Receiver, sender: Sender, temperature_delta=0.000001, humidity_delta=0.0000001):
        self.thermometer = thermometer
        self.humidity_sensor = humidity_sensor
        self.barometer = barometer
        self.is_thermostat_on = False
        self.is_dryer_on = False
        self.current_temperature = 20 # thermometer.current_temperature(*time_now())
        self.current_humidity = 0.3 # humidity_sensor.current_humidity(*time_now())
        self.receiver = receiver
        self.sender = sender
        self.temperature_delta = temperature_delta
        self.humidity_delta = humidity_delta

        with open('config.json') as file:
            config = json.load(file)
            self.name = config['name']

        self.last_sent, _, _ = time_now()

    def __update_temperature(self):
        time, day, month = time_now()
        temp = self.thermometer.current_temperature(time, day, month)
        temp_change = 0.0

        if self.is_thermostat_on:
            temp_change = (self.temperature_delta * random.random())
        elif self.current_temperature < temp:
            temp_change = (self.temperature_delta * random.random())
        else:
            temp_change = -1 * (self.temperature_delta * random.random())

        self.current_temperature = min(self.current_temperature + temp_change, 40)

    def __update_humidity(self):
        time, day, month = time_now()
        humidity = self.humidity_sensor.current_humidity(time, day, month)
        humidity_change = 0

        if self.is_dryer_on:
            humidity_change -= (self.humidity_delta * random.random())
            self.current_humidity = min(max(self.current_humidity - humidity_change, 0), 1)
        elif self.current_humidity < humidity:
            humidity_change = (self.humidity_delta * random.random())
            self.current_humidity = min(max(self.current_humidity + humidity_change, 0), 1)
        else:
            humidity -= (self.humidity_delta * random.random())
            self.current_humidity = min(max(self.current_humidity - humidity_change, 0), 1)

    def update_all_parameters(self):
        self.__update_humidity()
        self.__update_temperature()

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

    def sending(self, delay=MINUTE_1):
        self.sender.connect_to_broker()
        while True:
            t_now, day, month = time_now()
            if t_now - self.last_sent > delay:
                self.send_message(t_now, day, month)
                self.last_sent = t_now
            elif self.last_sent - t_now > 23:
                self.send_message(t_now, day, month)
                self.last_sent = t_now

    def send_message(self, time, day, month):
        temp = round(self.current_temperature, 3)
        hum = round(self.current_humidity, 2)
        pres = self.barometer.current_pressure(time, day, month)
        self.sender.publish(f"{self.name}#{temp}#{hum}#{pres}")
        print(f'{self.name}\n{temp}C\n{hum * 100}%\n{pres}hPa')

    def start(self):
        while True:
            self.update_all_parameters()


def main():
    tempParams = TemperatureParams(0.3)
    humParams = HumidityParams(0, 0.78, 0.01, tempParams)
    presParams = PressureParams(970, 1020, 1)
    therm = Thermometer(tempParams)
    humSensor = HumiditySensor(humParams)
    barom = Barometer(presParams)
    sender = Sender(SERVER_IP, ROOM_DATA)
    receiver = Receiver(SERVER_IP, DIRECTIVES)
    room = Room(therm, humSensor, barom, receiver, sender, temperature_delta=0.00001, humidity_delta=0.00001)
    Thread(target=lambda: room.listening()).start()
    Thread(target=lambda: room.sending(delay=Room.SECONDS_15)).start()
    while True:
        room.start()


if __name__ == '__main__':
    main()





