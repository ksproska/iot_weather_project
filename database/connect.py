import sqlite3
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
    def __init__(self, database_filename="weather_project.db"):
        self.__connection = sqlite3.connect(database_filename)
        self.__cursor = self.__connection.cursor()

    def commit(self):
        self.__connection.commit()

    def __run_lines_with_single_display(self, *lines):
        for line in lines:
            print_heading(f'EXECUTING LINE:')
            print(line)
            try:
                self.__cursor.execute(line)
            except Exception as e:
                print_error(f'ERROR: {e}')
        self.commit()

    def drop_tables(self):
        all_commands = all_commands_from_file('drop_tables.sql')
        self.__run_lines_with_single_display(*all_commands)

    def init_tables(self):
        all_commands = all_commands_from_file('init_tables.sql')
        self.__run_lines_with_single_display(*all_commands)

    def add_object(self, addable_object: AddableToDatabase):
        result = self.__cursor.execute(addable_object.sql_addable)
        self.commit()
        return result.fetchone() is None

    def __get_all_objects(self, class_type, extra_conditions='') -> list:
        command = f'SELECT ' + ', '.join([str(x) for x in class_type.colums_order()]) \
                  + f' FROM {class_type.__name__}{extra_conditions};'
        all_objects = []
        result = self.__cursor.execute(command).fetchall()
        for row in result:
            all_objects.append(class_type(*row))
        return all_objects

    def __get_current_preference(self, class_type, room_name: str):
        current = self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                         f'AND time(\'now\', \'localtime\') BETWEEN time_start AND time_end '
                                                         f'AND ('
                                                             f'weight={class_type.WEIGHT_TEMPORARY} '
                                                             f'AND datetime(\'now\', \'localtime\') - preference_timestamp <= {class_type.TTL.seconds} '
                                                             f'OR ('
                                                                 f'weight={class_type.WEIGHT_DEFAULT} '
                                                                 f'OR weight = {class_type.WEIGHT_SCHEDULE}'
                                                             f')'
                                                         f') '
                                                     f'ORDER BY weight DESC, '
                                                        f'preference_timestamp DESC')
        # [print(x) for x in current]
        return current[0]

    def __get_default_preference(self, class_type, room_name: str):
        current = self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                         f'AND weight={class_type.WEIGHT_DEFAULT} '
                                                     f'ORDER BY preference_timestamp DESC')
        # [print(x) for x in current]
        return current[0]

    def __get_all_scheduled_preferences(self, class_type, room_name: str) -> list:
        return self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                    f'AND weight = {class_type.WEIGHT_SCHEDULE} '
                                                  f'ORDER BY time_start ASC')

    def get_all_records(self, room_name: str, newest_to_oldest=True):
        if newest_to_oldest:
            order = 'DESC'
        else:
            order = 'ASC'
        return self.__get_all_objects(Record, f' WHERE room_name=\'{room_name}\' '
                                              f'ORDER BY record_time {order}')

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

    def default_preference_temperature(self, room_name: str) -> float:
        return self.__get_default_preference(Preference_temperature, room_name).value

    def default_preference_humidity(self, room_name: str):
        return self.__get_default_preference(Preference_humidity, room_name).value
