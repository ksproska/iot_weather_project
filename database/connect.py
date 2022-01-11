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

    def get_all_records(self, room_name: str):
        return self.__get_all_objects(Record, f' WHERE room_name=\'{room_name}\' '
                                                  f'ALLOW FILTERING')

    def get_all_scheduled_preferences_temperature(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preference_temperature, room_name)

    def get_all_scheduled_preferences_humidity(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preference_humidity, room_name)

    @property
    def all_preferences_temperature(self):
        return self.__get_all_objects(Preference_temperature)

    @property
    def all_preferences_humidity(self):
        return self.__get_all_objects(Preference_humidity)

    @property
    def all_records(self):
        return self.__get_all_objects(Record)

    def current_preference_temperature(self, room_name: str) -> float:
        return self.__get_current_preference(Preference_temperature, room_name).value

    def current_preference_humidity(self, room_name: str):
        return self.__get_current_preference(Preference_humidity, room_name).value
