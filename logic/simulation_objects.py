import math
import datetime
import matplotlib.pyplot as pyl
import numpy as np
import random

# Funkcja napisana tak by przyspieszyć wyniki symulacji (1 h = 2.5 min w rzeczywistości)
def get_time():
    now = datetime.datetime.now()
    hour = now.minute * 24 / 60 # Funkcja mapująca minuty na godziny (dla celów symulacji)
    minute = now.second / 2.5
    return round(hour + minute / 60, 3)


class TemperatureParams:
    def __init__(self, min_temp, max_temp, temp_fluctuation):
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.temp_fluctuation = temp_fluctuation

    def __norm_sin(self, x):
        return (math.sin(x) + 1) / 2

    def current_temperature(self, time):
        fluctuation = random.random() * self.temp_fluctuation
        sign = random.randint(0, 3) - 1
        return (self.max_temp - self.min_temp) * self.__norm_sin(math.pi * (time - 9) / 12) + self.min_temp + (sign * fluctuation)


class HumidityParams:
    def __init__(self, min_hum, max_hum, hum_fluctuation, temp_params):
        self.max_humidity = max_hum
        self.min_humidity = min_hum
        self.humidity_fluctuation = hum_fluctuation
        self.temp_parameters = temp_params

    def current_humidity(self, time):
        temp = self.temp_parameters.current_temperature(time)
        temp_amplitude = self.temp_parameters.max_temp - self.temp_parameters.min_temp
        percentage = (temp - self.temp_parameters.min_temp) / temp_amplitude
        sign = random.randint(0, 3) - 1
        fluctuation = random.random() * self.humidity_fluctuation
        read = 1 - (self.max_humidity - self.min_humidity) * percentage + sign * fluctuation
        return min(max(0, read), 1)


class Thermometer:
    def __init__(self, params: TemperatureParams):
        self.parameters = params

    def plot(self):
        x = np.arange(0, 24, 0.1)
        y = np.array([self.parameters.current_temperature(elem) for elem in x])
        pyl.plot(x, y)
        pyl.show()


class HumiditySensor:
    def __init__(self, params: HumidityParams):
        self.parameters = params

    def plot(self):
        x = np.arange(0, 24, 0.1)
        y = np.array([self.current_humidity(elem) for elem in x])
        pyl.plot(x, y)
        pyl.show()



