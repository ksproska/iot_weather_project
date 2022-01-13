import sqlite3
from database.tables_as_classes import *


def print_error(message):
    print(f'\033[91m{message}\033[0m')


def print_heading(message):
    print(f'\n\033[95m{message}\033[0m')


def all_commands_from_file(filename):
    """
    :param filename: file containing queries to be executed
    :return: list[str] of queries
    """
    all_queries = []
    with open(filename, 'r', encoding='utf-8') as f:
        full_command = []
        for command in f.readlines():
            full_command.append(command.replace('\n', ''))
            if full_command[-1].endswith(';'):
                all_queries.append('\n'.join(full_command))
                full_command = []
    return all_queries


class Connection:
    def __init__(self, database_filename="weather_project.db"):
        """
        Establishing connection for database, necessary for executing any queries.

        :param database_filename: path to database, creates new if doesn't exist
        """
        self.__connection = sqlite3.connect(database_filename)
        self.__cursor = self.__connection.cursor()

    def execute(self, query_command):
        """
        Changes will not be saved if commit is not run afterwards.
        """
        return self.__cursor.execute(query_command)

    def commit(self):
        self.__connection.commit()

    def __run_lines_with_single_display(self, *lines):
        for line in lines:
            print_heading(f'EXECUTING LINE:')
            print(line)
            try:
                self.execute(line)
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
        """
        :param addable_object: object inheriting from AddableToDatabase
        """
        self.execute(addable_object.sql_addable)
        self.commit()

    def __get_all_objects(self, class_type, extra_conditions='') -> list:
        """
        :param class_type: object inheriting from AddableToDatabase
        :param extra_conditions: rest of the query after SELECT {col1, col2, ...} FROM {tablename}
        :return: list[class_type]
        """
        command = f'SELECT ' + ', '.join([str(x) for x in class_type.colums_order()]) \
                  + f' FROM {class_type.__name__}{extra_conditions};'
        all_objects = []
        result = self.execute(command).fetchall()
        for row in result:
            all_objects.append(class_type(*row))
        return all_objects

    def __get_current_preference(self, class_type, room_name: str):
        """
        Rules for accessing current:

        + time_start <= now() <= time_end

        + for Temporary: now() - timestamp <= TTL

        :param class_type: object inheriting from Preference
        :param room_name: name of a room for WHERE condition
        :return: object of type class_type
        """
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
        """
            The most recent (preference_timestamp) with weight DEFAULT

            :param class_type: object inheriting from Preference
            :param room_name: name of a room for WHERE condition
            :return: object of type class_type
        """
        current = self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                         f'AND weight={class_type.WEIGHT_DEFAULT} '
                                                     f'ORDER BY preference_timestamp DESC')
        # [print(x) for x in current]
        return current[0]

    def __get_all_scheduled_preferences(self, class_type, room_name: str) -> list:
        """
            List of objects of class class_type, with weight SCHEDULE, sorted by time_start

            :param class_type: object inheriting from Preference
            :param room_name: name of a room for WHERE condition
            :return: list[class_type]
        """
        return self.__get_all_objects(class_type, f' WHERE room_name=\'{room_name}\' '
                                                    f'AND weight = {class_type.WEIGHT_SCHEDULE} '
                                                  f'ORDER BY time_start ASC')

    def get_all_records(self, room_name: str, newest_to_oldest=True):
        """
        :param room_name: name of a room for WHERE condition
        :param newest_to_oldest: sorting order
        :return: list[Record] sorted according to newest_to_oldest
        """
        if newest_to_oldest:
            order = 'DESC'
        else:
            order = 'ASC'
        return self.__get_all_objects(Record, f' WHERE room_name=\'{room_name}\' '
                                              f'ORDER BY record_time {order}')

    # getters for all for each table ___________________________________________________________________________________
    @property
    def all_preferences_temperature(self):
        return self.__get_all_objects(Preference_temperature)

    @property
    def all_preferences_humidity(self):
        return self.__get_all_objects(Preference_humidity)

    @property
    def all_records(self):
        return self.__get_all_objects(Record)

    # getters for scheduled preferences ________________________________________________________________________________
    def get_all_scheduled_preferences_temperature(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preference_temperature, room_name)

    def get_all_scheduled_preferences_humidity(self, room_name: str):
        return self.__get_all_scheduled_preferences(Preference_humidity, room_name)

    # different preferences value getters ______________________________________________________________________________
    def current_preference_temperature(self, room_name: str) -> float:
        return self.__get_current_preference(Preference_temperature, room_name).value

    def current_preference_humidity(self, room_name: str) -> float:
        return self.__get_current_preference(Preference_humidity, room_name).value

    def default_preference_temperature(self, room_name: str) -> float:
        return self.__get_default_preference(Preference_temperature, room_name).value

    def default_preference_humidity(self, room_name: str) -> float:
        return self.__get_default_preference(Preference_humidity, room_name).value
