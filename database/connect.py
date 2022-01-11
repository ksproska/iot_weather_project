import unittest

import cassandra
# pip install cassandra-driver
from cassandra.cluster import Cluster, ResponseFuture, ResultSet

from database.tables_as_classes import *


def print_error(message):
    print(f'\033[91m{message}\033[0m')


def print_heading(message):
    print(f'\n\033[95m{message}\033[0m')


def all_commands_from_file(filename):
    all_init_commands = []
    with open(filename, 'r', encoding='utf-8') as f:
        full_command = []
        for command in f.readlines():
            full_command.append(command.replace('\n', ''))
            if full_command[-1].endswith(';'):
                all_init_commands.append('\n'.join(full_command))
                full_command = []
    return all_init_commands


class Connection:
    def __init__(self, database_name='weather_project'):
        cluster = Cluster()
        self.__session = cluster.connect(database_name, wait_for_all_pools=True)
        self.__session.execute(f'USE {database_name}')

    def __run_lines_with_single_display(self, *lines):
        for line in lines:
            print_heading(f'EXECUTING LINE:')
            print(line)
            try:
                result: ResultSet = self.__session.execute(line)
            except Exception as e:
                print_error(f'ERROR: {e}')

    def drop_tables(self):
        all_drop = all_commands_from_file('drop_tables.cql')
        self.__run_lines_with_single_display(*all_drop)

    def init_tables(self):
        all_drop = all_commands_from_file('init_tables.cql')
        self.__run_lines_with_single_display(*all_drop)

    def add_object(self, addable_object: AddableToDatabase):
        try:
            # print(addable_object.sql_addable)
            result: ResultSet = self.__session.execute(addable_object.sql_addable)
            return result.one() is None
        except Exception:
            return False

    def __get_all_objects(self, class_type, extra_conditions='') -> list:
        command = f'SELECT ' + ', '.join([str(x) for x in class_type.colums_order()]) \
                  + f' FROM {class_type.__name__}{extra_conditions};'
        # print(command)
        all_objects = []
        try:
            result: ResultSet = self.__session.execute(command)
            for row in result:
                all_objects.append(class_type(*row))
        except Exception:
            pass
        return all_objects

    def __get_current_preference(self, class_type, room_name: str):
        time_now = str(datetime.now().time()) + '000'
        current = self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                   f'AND time_start < \'{time_now}\' '
                                                   f'AND time_end > \'{time_now}\' '
                                                   f'ORDER BY weight DESC '
                                                   f'LIMIT 1 '
                                                   f'ALLOW FILTERING')
        return current[0]

    def __get_all_scheduled_preferences(self, class_type, room_name: str) -> list:
        return self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                   f'AND weight = {class_type.WEIGHT_SCHEDULE} '
                                                   f'ALLOW FILTERING')

    def get_all_scheduled_preferences_temperature(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preferences_temperature, room_name)

    def get_all_scheduled_preferences_humidity(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preferences_humidity, room_name)

    @property
    def all_preferences_temperature(self):
        return self.__get_all_objects(Preferences_temperature)

    @property
    def all_preferences_humidity(self):
        return self.__get_all_objects(Preferences_humidity)

    @property
    def all_records(self):
        return self.__get_all_objects(Records)

    def current_preference_temperature(self, room_name: str) -> float:
        return self.__get_current_preference(Preferences_temperature, room_name).value

    def current_preference_humidity(self, room_name: str):
        return self.__get_current_preference(Preferences_humidity, room_name).value


class DBTest(unittest.TestCase):
    ROOM_NAMES = ['kitchen', 'living room', 'bedroom']

    def setUp(self) -> None:
        self.connection = Connection()

    def test_init(self):
        self.connection.drop_tables()
        self.connection.init_tables()

    def test_add_and_display_records(self):
        for room_name in self.ROOM_NAMES:
            self.connection.add_object(Records.with_current_time(room_name, 19.3, 35.2, 1000, True, False))
        [print(x) for x in self.connection.all_records]

    def test_adding_preference_temperature_temp(self):
        pref = Preferences_temperature.as_temporary(21.3, 'kitchen')
        print(f'ADDED: {self.connection.add_object(pref)}')

    def test_example_setup(self):
        self.connection.drop_tables()
        self.connection.init_tables()
        for room_name in self.ROOM_NAMES:
            self.connection.add_object(Preferences_temperature.as_default(21.3, room_name))
            self.connection.add_object(Preferences_temperature.as_schedule(11.0, room_name,
                                                                           get_time(0), get_time(11, 30)))
            self.connection.add_object(Preferences_temperature.as_schedule(15.0, room_name,
                                                                           get_time(15), get_time(18, 30)))
            self.connection.add_object(Preferences_temperature.as_temporary(21.3, room_name))

            self.connection.add_object(Preferences_humidity.as_default(45, room_name))
            self.connection.add_object(Preferences_humidity.as_schedule(40.0, room_name,
                                                                        get_time(15), get_time(18, 30)))
            self.connection.add_object(Preferences_humidity.as_temporary(44, room_name))

        print_heading('PREFERENCES TEMPERATURE')
        [print(x) for x in self.connection.all_preferences_temperature]
        print_heading('PREFERENCES HUMIDITY')
        [print(x) for x in self.connection.all_preferences_humidity]

        for room_name in self.ROOM_NAMES:
            print_heading(f'CURRENT DEFAULTS FOR {room_name}: ')
            print(f'temperature: {self.connection.current_preference_temperature(room_name)}')
            print(f'humidity:    {self.connection.current_preference_humidity(room_name)}')

    def test_display_all_scheduled_preferences_temperature(self):
        print_heading('PREFERENCES TEMPERATURE for kitchen')
        preferences_tem = self.connection.get_all_scheduled_preferences_temperature('kitchen')
        [print(x) for x in preferences_tem]
        print_heading('PREFERENCES HUMIDITY for kitchen')
        preferences_tem = self.connection.get_all_scheduled_preferences_humidity('kitchen')
        [print(x) for x in preferences_tem]

    def test_display_current_preference_temperature(self):
        print_heading(f'CURRENT DEFAULTS FOR kitchen: ')
        print(f'temperature: {self.connection.current_preference_temperature("kitchen")}')
        print(f'humidity:    {self.connection.current_preference_humidity("kitchen")}')
