import sys
# sys.path.append('path')
SERVER_IP = '25.33.38.163'
from logic.environment.simulation_objects import Thermometer, HumiditySensor, Barometer, PressureParams, \
    TemperatureParams, HumidityParams
from logic.communication.receiver import Receiver
from logic.communication.sender import Sender
from logic.communication.constants import *
from threading import Thread
from logic.environment.simulation_objects import simulated_time, normal_time
import random
import datetime
import json
import tkinter as tk
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
        self.current_temperature = 20  # thermometer.current_temperature(*time_now())
        self.current_humidity = 0.3  # humidity_sensor.current_humidity(*time_now())
        self.current_pressure = barometer.current_pressure(0, 0, 0)
        self.receiver = receiver
        self.sender = sender
        self.temperature_delta = temperature_delta
        self.humidity_delta = humidity_delta

        with open('config.json') as file:
            config = json.load(file)
            self.name = config['name']

        self.last_sent, _, _ = time_now()

        self.__make_gui()

    def __make_gui(self):
        self.__prepare_tkinter_parameters()
        self.__prepare_window_labels()
        self.__prepare_window_buttons()

    def __prepare_tkinter_parameters(self):
        self.__FONT = ('Weibei', 14)
        self.__BG_COLOR = '#3a3a3a'
        self.__FG_COLOR = 'white'
        self.__ON_COLOR = '#009900'
        self.__OFF_COLOR = '#cc0000'
        self.tk = tk.Tk()
        self.tk.title(f'Room: {self.name}')
        self.tk.geometry('501x122')
        self.temperature_text = tk.StringVar(self.tk, f'Temperature: {round(self.current_temperature)}°C')
        self.temperature_setup_text = tk.StringVar(self.tk, f'{round(self.current_temperature)}')
        self.humidity_text = tk.StringVar(self.tk, f'Humidity: {round(self.current_humidity * 100)}%')
        self.pressure_text = tk.StringVar(self.tk, f'Pressure: {round(self.current_pressure)} hPa')
        self.thermostat_state = tk.BooleanVar(self.tk, self.is_thermostat_on)
        self.dryer_state = tk.BooleanVar(self.tk, self.is_dryer_on)

    def __prepare_window_labels(self):
        self.name_label = tk.Label(self.tk, text=self.name, font=self.__FONT, anchor='w', fg=self.__FG_COLOR,
                                   bg=self.__BG_COLOR)
        self.name_label.grid(row=0, column=0, columnspan=6, sticky='NEWS')

        self.temperature_label = tk.Label(self.tk, textvariable=self.temperature_text, font=self.__FONT,
                                          anchor='w', fg=self.__FG_COLOR, bg=self.__BG_COLOR)
        self.temperature_label.grid(row=1, column=0, sticky='NEWS')

        self.temperature_setup_label = tk.Label(self.tk, textvariable=self.temperature_setup_text, font=self.__FONT,
                                                anchor='center', fg=self.__FG_COLOR, bg=self.__BG_COLOR,
                                                width='5')
        self.temperature_setup_label.grid(row=1, column=3, sticky='NEWS')

        self.humidity_label = tk.Label(self.tk, textvariable=self.humidity_text, font=self.__FONT, anchor='w',
                                       fg=self.__FG_COLOR, bg=self.__BG_COLOR)
        self.humidity_label.grid(row=2, column=0, sticky='NEWS')

        self.pressure_label = tk.Label(self.tk, textvariable=self.pressure_text, font=self.__FONT, anchor='w',
                                       fg=self.__FG_COLOR, bg=self.__BG_COLOR)
        self.pressure_label.grid(row=3, column=0, sticky='NEWS')

        self.is_thermostat_on_label = tk.Label(self.tk, width='10',
                                               bg=self.__ON_COLOR if self.is_thermostat_on else self.__OFF_COLOR)
        self.is_thermostat_on_label.grid(row=1, column=1, sticky='NEWS')

        self.is_dryer_on_label = tk.Label(self.tk, width='10',
                                          bg=self.__ON_COLOR if self.is_dryer_on else self.__OFF_COLOR)
        self.is_dryer_on_label.grid(row=2, column=1, sticky='NEWS')

        self.empty_humidity_label = tk.Label(self.tk, width='10', bg=self.__BG_COLOR)
        self.empty_humidity_label.grid(row=2, column=2, columnspan=4, sticky='NEWS')
        self.empty_pressure_label = tk.Label(self.tk, width='10', bg=self.__BG_COLOR)
        self.empty_pressure_label.grid(row=3, column=1, columnspan=5, sticky='NEWS')

    def __prepare_window_buttons(self):
        self.thermostat_set_button = tk.Button(self.tk, bg=self.__BG_COLOR, fg=self.__FG_COLOR, anchor='center',
                                               width='5', command=lambda: self.send_user_preferred_temperature(),
                                               font=self.__FONT, text='SET')
        self.thermostat_set_button.grid(row=1, column=5, sticky='NEWS')
        self.increase_temperature_button = tk.Button(self.tk, width='5', font=self.__FONT, text='+',
                                                     command=lambda: self.__increase_displayed_temperature(),
                                                     fg=self.__FG_COLOR, bg=self.__BG_COLOR)
        self.increase_temperature_button.grid(row=1, column=4, sticky='NEWS')
        self.decrease_temperature_button = tk.Button(self.tk, width='5', font=self.__FONT, text='-',
                                                     command=lambda: self.__decrease_displayed_temperature(),
                                                     fg=self.__FG_COLOR, bg=self.__BG_COLOR)
        self.decrease_temperature_button.grid(row=1, column=2, sticky='NEWS')

    def __increase_displayed_temperature(self):
        now = int(self.temperature_setup_text.get())
        if now < 40:
            self.temperature_setup_text.set(f'{now+1}')

    def __decrease_displayed_temperature(self):
        now = int(self.temperature_setup_text.get())
        if now > 1:
            self.temperature_setup_text.set(f'{now - 1}')

    def __update_diodes_status(self):
        if self.is_thermostat_on:
            self.is_thermostat_on_label.config(bg=self.__ON_COLOR)
        else:
            self.is_thermostat_on_label.config(bg=self.__OFF_COLOR)
        if self.is_dryer_on:
            self.is_dryer_on_label.config(bg=self.__ON_COLOR)
        else:
            self.is_dryer_on_label.config(bg=self.__OFF_COLOR)

    def __update_labels_status(self):
        self.temperature_text.set(f'Teperature: {round(self.current_temperature, 1)}°C')
        self.humidity_text.set(f'Humidity: {round(self.current_humidity * 100)}%')
        self.pressure_text.set(f'Pressure: {round(self.current_pressure)} hPa')

    def __update_temperature(self):
        time, day, month = time_now()
        temp = self.thermometer.current_temperature(time, day, month)

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
        humidity_change = self.humidity_delta * random.random()
        if self.is_dryer_on:
            self.current_humidity = min(max(self.current_humidity - humidity_change, 0), 1)
        elif self.current_humidity < humidity:
            self.current_humidity = min(max(self.current_humidity + humidity_change, 0), 1)
        else:
            self.current_humidity = min(max(self.current_humidity - humidity_change, 0), 1)

    def update_all_parameters(self):
        self.__update_humidity()
        self.__update_temperature()
        self.__update_labels_status()
        self.__update_diodes_status()
        self.tk.after(5, lambda: self.update_all_parameters())

    def update_devices(self, message):
        name, is_thermostat_on, is_dryer_on = self.__decode_message(message.payload.decode('utf-8'))
        if name.upper() == self.name.upper():
            self.is_dryer_on = is_dryer_on
            self.is_thermostat_on = is_thermostat_on
            self.__update_diodes_status()
            # print(f'device updated:\nThermostat on: {self.is_thermostat_on}\nDryer on: {self.is_dryer_on}\n')

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
        self.current_pressure = pres
        self.sender.publish(f"{self.name}#{temp}#{hum}#{pres}")

    def send_user_preferred_temperature(self):
        self.sender.publish(f'{self.name}#THERM#{self.temperature_setup_text.get()}')

    def start(self):
        self.update_all_parameters()
        self.tk.mainloop()


def main():
    tempParams = TemperatureParams(0.3)
    humParams = HumidityParams(0, 0.78, 0.01, tempParams)
    presParams = PressureParams(970, 1020, 1)
    therm = Thermometer(tempParams)
    humSensor = HumiditySensor(humParams)
    barom = Barometer(presParams)
    sender = Sender(SERVER_IP, ROOM_DATA)
    receiver = Receiver(SERVER_IP, DIRECTIVES)
    room = Room(therm, humSensor, barom, receiver, sender, temperature_delta=0.0003, humidity_delta=0.0003)
    # Thread(target=lambda: room.listening()).start()
    # Thread(target=lambda: room.sending(delay=Room.SECONDS_15)).start()
    room.start()


if __name__ == '__main__':
    main()
