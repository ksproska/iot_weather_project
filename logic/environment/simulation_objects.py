import math
import datetime
import matplotlib.pyplot as pyl
import numpy as np
import random


# Funkcja napisana tak by przyspieszyć wyniki symulacji (1 h = 2.5 min w rzeczywistości)
# def get_time():
#     now = datetime.datetime.now()
#     hour = now.minute * 24 / 60  # Funkcja mapująca minuty na godziny (dla celów symulacji)
#     minute = now.second / 2.5
#     return round(hour + minute / 60, 3)

def normal_time() -> (float, int, int):
    date_now = datetime.datetime.now()
    day = date_now.day
    month = date_now.month
    hour = date_now.hour + date_now.minute / 60
    return round(hour, 4), day, month


def simulated_time(month=1) -> (float, int, int):
    date_now = datetime.datetime.now()
    real_seconds = date_now.minute * 60 + date_now.second
    day = int(real_seconds / 120)  # day indeed from 0
    real_seconds -= day * 120
    hour = real_seconds / 5
    return round(hour, 4), day + 1, month


class TemperatureParams:

    __DEFAULT_TEMPERATURES = [12, -3.3, -2.1, 1.9, 7.7, 13.5, 16.7, 18, 17.3, 13.1, 8.2, 3.2, -0.9]
    __DEFAULT_AMPLITUDES = [0, 5.1, 6.2, 8.1, 9.9, 9.5, 9.1, 8.8, 9.1, 8.3, 7, 5.3, 4.5]

    def __init__(self, temp_fluctuation, month_amplitudes=None, month_temperatures=None):
        # self.max_temp = max_temp
        # self.min_temp = min_temp
        self.temp_fluctuation = temp_fluctuation
        if month_amplitudes is None:
            self.month_amplitudes = self.__DEFAULT_AMPLITUDES
        else:
            self.month_amplitudes = month_amplitudes

        if month_temperatures is None:
            self.month_temperatures = self.__DEFAULT_TEMPERATURES
        else:
            self.month_temperatures = month_temperatures

    def __norm_sin(self, x):
        return (math.sin(x) + 1) / 2

    def current_temperature(self, time: float, day: int, month: int):
        fluctuation = random.random() * self.temp_fluctuation
        sign = random.randint(0, 3) - 1
        temp_min = self.min_temp(day, month)
        temp_max = self.max_temp(day, month)
        return (temp_max - temp_min) * self.__norm_sin(math.pi * (time - 9) / 12) + temp_min + (sign * fluctuation)

    def max_temp(self, day, month):
        avg = self.__get_balanced_average_temperature(day, month)
        return avg + self.month_amplitudes[month] / 2

    def min_temp(self, day, month):
        avg = self.__get_balanced_average_temperature(day, month)
        return avg - self.month_amplitudes[month] / 2

    def __get_balanced_average_temperature(self, day, month):
        current_avg = self.month_temperatures[month]
        if day < 15:
            current_weight = day / 15
            previous_weight = 1 - current_weight
            prev_avg = self.__prev_avg_temp(month)
            return (current_avg * (current_weight + 1) + prev_avg * previous_weight) / 2
        elif day > 15:
            next_weight = (day - 15) / 15
            current_weight = 1 - next_weight
            next_avg = self.__next_avg_temp(month)
            return ((current_weight + 1) * current_avg + next_weight * next_avg) / 2
        else:
            return self.month_temperatures[month]

    def __prev_avg_temp(self, month):
        if month == 1:
            return self.month_temperatures[-1]
        else:
            return self.month_temperatures[month - 1]

    def __next_avg_temp(self, month):
        if month == 12:
            return self.month_temperatures[1]
        else:
            return self.month_temperatures[month + 1]


class HumidityParams:
    def __init__(self, min_hum, max_hum, hum_fluctuation, temp_params: TemperatureParams):
        self.max_humidity = max_hum
        self.min_humidity = min_hum
        self.humidity_fluctuation = hum_fluctuation
        self.temp_parameters = temp_params

    def current_humidity(self, time: float, day: int, month: int):
        temp = self.temp_parameters.current_temperature(time, day, month)
        temp_amplitude = self.temp_parameters.month_amplitudes[month]
        percentage = (temp - self.temp_parameters.min_temp(day, month)) / temp_amplitude
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

    def current_pressure(self, time, day, month):
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

    def current_temperature(self, time: float, day: int, month: int):
        return self.parameters.current_temperature(time, day, month)


class HumiditySensor:
    def __init__(self, params: HumidityParams):
        self.parameters = params

    def current_humidity(self, time: float, day: int, month: int):
        return self.parameters.current_humidity(time, day, month)


class Barometer:
    def __init__(self, params: PressureParams):
        self.parameters = params

    def current_pressure(self, time: float, day: int, month: int):
        self.parameters.current_pressure(time, day, month)






