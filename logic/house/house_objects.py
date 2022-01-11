from logic.environment.simulation_objects import Thermometer, HumiditySensor, get_time, TemperatureParams, HumidityParams
from logic.communication.receiver import Receiver
from logic.communication.sender import Sender
from logic.communication.constants import *
from threading import Thread
from logic.environment.simulation_objects import get_time
import random
import datetime
from time import sleep


class Room:
    def __init__(self, idx: int, thermometer: Thermometer, humidity_sensor: HumiditySensor,
                 receiver: Receiver, sender: Sender, name="", temperature_delta=0.2, humidity_delta=0.05):
        self.id = idx
        self.thermometer = thermometer
        self.humidity_sensor = humidity_sensor
        self.name = name
        self.is_thermostat_on = False
        self.is_dryer_on = False
        self.current_temperature = thermometer.current_temperature(get_time())
        self.current_humidity = humidity_sensor.current_humidity(get_time())
        self.receiver = receiver
        self.sender = sender
        self.temperature_delta = temperature_delta
        self.humidity_delta = humidity_delta
        self.last_measurement = datetime.datetime.now()

    def update_temperature(self):
        # Używamy funkcji get_time dla szybkiej symulacji a funkcji datetime.now() dla czasu rzeczywistego
        # time = get_time()
        time_now = datetime.datetime.now()
        time = time_now.hour + time_now.minute / 60
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
        # Używamy funkcji get_time dla szybkiej symulacji a funkcji datetime.now() dla czasu rzeczywistego
        # time = get_time()
        time_now = datetime.datetime.now()
        time = time_now.hour + time_now.minute / 60
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
        print('devices updated ' + message.payload.decode('utf-8'))

    def listen(self):
        self.receiver.connect_to_broker()
        self.receiver.loop_start()
        self.receiver.client.on_message = lambda client, userdata, message: self.update_devices(message)
        self.receiver.subscribe()
        while True:
            pass

    def send(self):
        self.sender.connect_to_broker()
        while True:
            sleep(2)
            time = get_time()
            temp = self.thermometer.current_temperature(time)
            hum = self.humidity_sensor.current_humidity(time)
            self.sender.publish(f"Temp = {temp}\nHum = {hum}")


if __name__ == '__main__':
    tempParams = TemperatureParams(10, 17, 0.3)
    humParams = HumidityParams(0, 0.78, 0.01, tempParams)
    thermometer = Thermometer(tempParams)
    humSensor = HumiditySensor(humParams)
    sender = Sender('localhost', ROOM_DATA) # ip do zmiany
    receiver = Receiver('localhost', DIRECTIVES) # ip do zmiany
    room = Room(1, thermometer, humSensor, receiver, sender, 'salon', temperature_delta=0.07, humidity_delta=0.02)
    Thread(target=lambda: room.listen()).start()
    Thread(target=lambda: room.send()).start()
    while True:
        pass





