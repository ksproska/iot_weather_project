from time import sleep
import unittest
from connect import *


class DBTest:
    ROOM_NAMES = ['kitchen', 'living room', 'bedroom']

    @classmethod
    def example_setup(cls):
        connection = Connection()
        connection.drop_tables()
        connection.init_tables_if_not_exist()
        print_heading('ADDING PREFERENCES')
        for room_name in cls.ROOM_NAMES:
            connection.add_object(Preference_temperature.as_default(21, room_name))
            connection.add_object(Preference_temperature.as_schedule(11.0, room_name,
                                                                          get_time(0), get_time(11, 30)))
            connection.add_object(Preference_temperature.as_schedule(15.0, room_name,
                                                                          get_time(15), get_time(18, 30)))
            connection.add_object(Preference_temperature.as_temporary(21.3, room_name))

            connection.add_object(Preference_humidity.as_default(45, room_name))
            connection.add_object(Preference_humidity.as_schedule(40.0, room_name,
                                                                       get_time(15), get_time(18, 30)))
            connection.add_object(Preference_humidity.as_temporary(44, room_name))

        for i in range(5):
            print_heading(f'{i}: ADDING RECORDS')
            for room_name in cls.ROOM_NAMES:
                connection.add_object(Record.with_current_time(room_name, 19.3, 35.2, 1000, True, False))
            sleep(2)
        connection.close()

    @classmethod
    def display_preferences(cls):
        connection = Connection()
        print_heading('all preferences TEMPERATURE')
        [print(x) for x in connection.all_preferences_temperature]
        print_heading('all preferences HUMIDITY')
        [print(x) for x in connection.all_preferences_humidity]

        for room_name in cls.ROOM_NAMES:
            print_heading(f'SCHEDULE {room_name} -----------------------------------------------------------------')
            print_heading(f'preferences TEMPERATURE')
            preferences_tem = connection.get_all_scheduled_preferences_temperature(room_name)
            [print(x) for x in preferences_tem]
            print_heading(f'preferences HUMIDITY')
            preferences_tem = connection.get_all_scheduled_preferences_humidity(room_name)
            [print(x) for x in preferences_tem]

        print_heading(f'CURRENT AIM -------------------------------------------------------------')
        for room_name in cls.ROOM_NAMES:
            print_heading(room_name)
            print(f'temperature: {connection.current_preference_temperature(room_name)}')
            print(f'humidity:    {connection.current_preference_humidity(room_name)}')

        print_heading(f'DEFAULT -----------------------------------------------------------------')
        for room_name in cls.ROOM_NAMES:
            print_heading(room_name)
            print(f'temperature: {connection.default_preference_temperature(room_name)}')
            print(f'humidity:    {connection.default_preference_humidity(room_name)}')
        connection.close()

    @classmethod
    def display_records(cls):
        connection = Connection()
        for room_name in cls.ROOM_NAMES:
            print_heading(f'{room_name}: RECORDINGS --------------------------------------------------------------')
            [print(x) for x in connection.get_all_records(room_name, newest_to_oldest=True)]
        connection.close()

    @classmethod
    def adding_preference_temperature_temp(cls):
        connection = Connection()
        for room_name in cls.ROOM_NAMES:
            connection.add_object(Preference_temperature.as_temporary(33.3, room_name))
            connection.add_object(Preference_humidity.as_temporary(77, room_name))
        connection.close()

    @classmethod
    def delete_examples(cls):
        connection = Connection()
        scheduled_humidity = connection.get_all_scheduled_preferences_humidity('kitchen')
        scheduled_temperature = connection.get_all_scheduled_preferences_temperature('kitchen')

        for preference in scheduled_humidity:
            connection.delete_preference(preference)

        for preference in scheduled_temperature:
            connection.delete_preference(preference)

        connection.close()

    @classmethod
    def grouped_by_examples(cls):
        connection = Connection()
        grouped_by_day = connection.get_records_grouped_by_day('kitchen')
        grouped_by_minute = connection.get_records_grouped_by_minute('kitchen')

        print_heading(f'GROUPED BY MINUTE --------------------------------------------------------------')
        for minute in grouped_by_minute:
            print(minute)
        print_heading(f'GROUPED BY DAY --------------------------------------------------------------')
        for day in grouped_by_day:
            print(day)

        connection.close()


if __name__ == '__main__':
    DBTest.example_setup()
    DBTest.display_preferences()
    DBTest.display_records()
    DBTest.delete_examples()
    DBTest.grouped_by_examples()

