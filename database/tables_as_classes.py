import inspect
from datetime import datetime, date, time, timedelta


class AddableToDatabase:
    @property
    def sql_addable(self):
        """
        example: "INSERT INTO ClassName (Atr_1, Atr_2) VALUES (Atr_1, Atr_2)"
        """
        keys = ', '.join(self.__dict__.keys())
        values = []
        for value in self.__dict__.values():
            if type(value) is str or type(value) is date or type(value) is time or type(value) is datetime:
                values.append(f'\'{value}\'')
            elif type(value) is set:
                values.append(f'{list(value)}')
            else:
                values.append(f'{value}')
        values_merged = ', '.join(values).replace('[', '{').replace(']', '}')
        return f'INSERT INTO \n{self.__class__.__name__} ({keys})\n VALUES \n({values_merged});\n'

    def __str__(self):
        all_merged = '\t'.join(f'{key}: \033[94m{self.__dict__[key]}\033[0m' for key in self.__dict__.keys())
        class_ = f'\033[96m{self.__class__.__name__.ljust(11)}\033[0m'
        return  f'{class_} {all_merged}'

    @classmethod
    def columns_order(cls):
        """
        :return: list of argument names for current class constructor in the order that they are required
        """
        return inspect.getfullargspec(cls).args[1:]


class Record(AddableToDatabase):
    def __init__(self, record_time, room_name, record_temp, record_humidity,
                 record_press, device_termost, device_dryer):
        self.record_time = record_time
        if type(record_time) is str:
            self.record_time = datetime.strptime(record_time, '%Y-%m-%d %H:%M:%S.%f')
        self.room_name = room_name
        self.record_temp = record_temp
        self.record_humidity = record_humidity
        self.record_press = record_press

        self.device_termost = device_termost
        self.device_dryer = device_dryer

    @classmethod
    def with_current_time(cls, room_name, record_temp, record_humidity,
                 record_press, device_termost, device_dryer):
        return cls(datetime.now(), room_name, record_temp, record_humidity, record_press, device_termost, device_dryer)


def get_time(hour, minutes = 0, sec = 0) -> time:
     return datetime.strptime(f'{hour:02}::{minutes:02}::{sec:02}',
                              '%H::%M::%S').time()


class Preference(AddableToDatabase):
    WEIGHT_DEFAULT = 0
    WEIGHT_SCHEDULE = 1
    WEIGHT_TEMPORARY = 2
    TTL = timedelta(minutes=20) # how long the temporary preference is deemed applicable

    def __init__(self, preference_timestamp, room_name, time_start, time_end, value, weight):
        self.weight = weight
        self.room_name = room_name
        self.value = value
        self.preference_timestamp = preference_timestamp
        if type(self.preference_timestamp) is str:
            self.record_time = datetime.strptime(preference_timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.time_start = time_start
        self.time_end = time_end

    @classmethod
    def as_default(cls, value, room_name):
        time_start = get_time(0)
        time_end = get_time(23, 59, 59)
        return cls(datetime.now(), room_name, time_start, time_end, value, cls.WEIGHT_DEFAULT)

    @classmethod
    def as_schedule(cls, value, room_name, time_start, time_end):
        return cls(datetime.now(), room_name, time_start, time_end, value, cls.WEIGHT_SCHEDULE)

    @classmethod
    def as_temporary(cls, value, room_name):
        safety_delta = timedelta(seconds=60)
        time_start = (datetime.now() - safety_delta)
        time_end = (time_start + safety_delta + cls.TTL).time()
        time_start = time_start.time()
        time_start = time_start.replace(microsecond=0)
        time_end = time_end.replace(microsecond=0)
        return cls(datetime.now(), room_name, time_start, time_end, value, cls.WEIGHT_TEMPORARY)

    # @property
    # def sql_addable(self):
    #     command = super().sql_addable
    #     if self.weight == self.WEIGHT_TEMPORARY:
    #         command = command[:-2] + f' USING TTL {self.TTL.seconds};\n'
    #     return command


class Preference_temperature(Preference):
    pass


class Preference_humidity(Preference):
    pass
