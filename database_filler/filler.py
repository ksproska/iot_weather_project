from database.connect import Connection
from database.tables_as_classes import Record
from logic.environment.simulation_objects import *
import datetime
import random

DATA_START = (datetime.datetime.now() - datetime.timedelta(days=1))
DATA_END = datetime.datetime.now()
DELTA_TIME = datetime.timedelta(minutes=1)

TEMP_START = 10
HUM_START = 0.2
TEMP_AIM = 22
HUM_AIM = 0.25

temperature = TemperatureParams(0.3)
humidity = HumidityParams(0, 0.78, 0.01, temperature)
pressure = PressureParams(970, 1020, 1)


def get_reading(prev_temp, prev_hum, temp_aim, hum_aim):
    if prev_temp < temp_aim:
        now_temp = prev_temp + 0.3 * random.random()
        is_therm_on = True
    else:
        now_temp = prev_temp - 0.3 * random.random()
        is_therm_on = False
    if prev_hum < hum_aim:
        now_hum = prev_hum + 0.2 * random.random()
        is_dryer_on = False
    else:
        now_hum = prev_hum - 0.2 * random.random()
        is_dryer_on = True
    pres = pressure.current_pressure(1, 1, 1)
    return round(now_temp, 3), round(now_hum, 2), int(pres), is_therm_on, is_dryer_on


def main():
    connection = Connection()
    current_time = DATA_START
    prev_records = [get_reading(TEMP_START, HUM_START, TEMP_AIM, HUM_AIM),
                    get_reading(TEMP_START, HUM_START, TEMP_AIM, HUM_AIM),
                    get_reading(TEMP_START, HUM_START, TEMP_AIM, HUM_AIM)]

    counter = 0
    start_datatime = datetime.datetime.now()
    while current_time < DATA_END:
        for inx, room_name in enumerate (['kitchen', 'bedroom', 'bathroom']):

            new_record = Record(record_time=current_time + datetime.timedelta(seconds=inx), room_name=room_name,
                                record_temp=prev_records[inx][0], record_humidity=prev_records[inx][1], record_press=prev_records[inx][2],
                                device_termost=prev_records[inx][3], device_dryer=prev_records[inx][4])
            if counter%60 == 0 and inx == 0:
                print(f'seconds: {(datetime.datetime.now() - start_datatime).seconds}')
                print(new_record)
            connection.add_object(new_record)
        counter += 1
        current_time += DELTA_TIME
        prev_records = [get_reading(prev_records[0][0], prev_records[0][1], TEMP_AIM, HUM_AIM),
                        get_reading(prev_records[1][0], prev_records[1][1], TEMP_AIM, HUM_AIM),
                        get_reading(prev_records[2][0], prev_records[2][1], TEMP_AIM, HUM_AIM)]
    connection.close()


if __name__ == '__main__':
    main()
