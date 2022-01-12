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


class PressureParams:
    def __init__(self, min_pres, max_pres, pres_fluctuation):
        self.min_pressure = min_pres
        self.max_pressure = max_pres
        self.pressure_fluctuation = pres_fluctuation
        middle = (self.max_pressure + self.min_pressure) / 2
        self.pressure_now = random.randint(middle - 20, middle + 20)

    def current_pressure(self, time):
        change = self.pressure_fluctuation * ((self.pressure_now - self.min_pressure) / (self.max_pressure - self.min_pressure))
        middle = (self.max_pressure + self.min_pressure) / 2

        if middle - 10 < self.pressure_now < middle + 10:
            sign = random.choice([0, 0, 0, 0, 0, 0, 0, 1, -1])
        elif self.pressure_now - 10 < middle:
            sign = random.randint(0, 4) - 1
        else:
            sign = random.randint(-1, 3) - 1
        new_pressure = max(min(self.pressure_now + sign * change, self.max_pressure), self.min_pressure)
        self.pressure_now = new_pressure
        return new_pressure


class Thermometer:
    def __init__(self, params: TemperatureParams):
        self.parameters = params

    def current_temperature(self, time):
        return self.parameters.current_temperature(time)


class HumiditySensor:
    def __init__(self, params: HumidityParams):
        self.parameters = params

    def current_humidity(self, time):
        return self.parameters.current_humidity(time)


class Barometer:
    def __init__(self, params: PressureParams):
        self.parameters = params

    def current_pressure(self, time):
        self.parameters.current_pressure(time)






