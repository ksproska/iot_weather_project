from time import sleep
import unittest
from connect import *


class DBTest(unittest.TestCase):
    ROOM_NAMES = ['kitchen', 'living room', 'bedroom']

    def setUp(self) -> None:
        self.connection = Connection()

    def test_example_setup(self):
        self.connection.drop_tables()
        self.connection.init_tables()
        print_heading('ADDING PREFERENCES')
        for room_name in self.ROOM_NAMES:
            self.connection.add_object(Preference_temperature.as_default(21, room_name))
            self.connection.add_object(Preference_temperature.as_schedule(11.0, room_name,
                                                                           get_time(0), get_time(11, 30)))
            self.connection.add_object(Preference_temperature.as_schedule(15.0, room_name,
                                                                           get_time(15), get_time(18, 30)))
            self.connection.add_object(Preference_temperature.as_temporary(21.3, room_name))

            self.connection.add_object(Preference_humidity.as_default(45, room_name))
            self.connection.add_object(Preference_humidity.as_schedule(40.0, room_name,
                                                                        get_time(15), get_time(18, 30)))
            self.connection.add_object(Preference_humidity.as_temporary(44, room_name))

        for i in range(5):
            print_heading(f'{i}: ADDING RECORDS')
            for room_name in self.ROOM_NAMES:
                self.connection.add_object(Record.with_current_time(room_name, 19.3, 35.2, 1000, True, False))
            sleep(2)

    def test_display_preferences(self):
        print_heading('all preferences TEMPERATURE')
        [print(x) for x in self.connection.all_preferences_temperature]
        print_heading('all preferences HUMIDITY')
        [print(x) for x in self.connection.all_preferences_humidity]

        for room_name in self.ROOM_NAMES:
            print_heading(f'SCHEDULE {room_name} -----------------------------------------------------------------')
            print_heading(f'preferences TEMPERATURE')
            preferences_tem = self.connection.get_all_scheduled_preferences_temperature(room_name)
            [print(x) for x in preferences_tem]
            print_heading(f'preferences HUMIDITY')
            preferences_tem = self.connection.get_all_scheduled_preferences_humidity(room_name)
            [print(x) for x in preferences_tem]

        for room_name in self.ROOM_NAMES:
            print_heading(f'{room_name}: CURRENT -----------------------------------------------------------------')
            print(f'temperature: {self.connection.current_preference_temperature(room_name)}')
            print(f'humidity:    {self.connection.current_preference_humidity(room_name)}')

    def test_display_records(self):
        for room_name in self.ROOM_NAMES:
            print_heading(f'{room_name}: RECORDINGS --------------------------------------------------------------')
            [print(x) for x in self.connection.get_all_records(room_name)]

    def test_adding_preference_temperature_temp(self):
        for room_name in self.ROOM_NAMES:
            self.connection.add_object(Preference_temperature.as_temporary(33.3, room_name))
            self.connection.add_object(Preference_humidity.as_temporary(77, room_name))
