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
    def colums_order(cls):
        return inspect.getfullargspec(cls).args[1:]


class Record(AddableToDatabase):
    def __init__(self, record_time: datetime, room_name: str, record_temp: float, record_humidity: float,
                 record_press: int, device_termost: bool, device_dryer: bool):
        self.record_time: datetime = record_time
        self.room_name: str = room_name
        self.record_temp: float = record_temp
        self.record_humidity: float = record_humidity
        self.record_press: int = record_press

        self.device_termost: bool = device_termost
        self.device_dryer: bool = device_dryer

    @classmethod
    def with_current_time(cls, room_name: str, record_temp: float, record_humidity: float,
                 record_press: int, device_termost: bool, device_dryer: bool):
        return cls(datetime.now(), room_name, record_temp, record_humidity, record_press, device_termost, device_dryer)


def get_time(hour: int, minutes: int = 0, sec: int = 0) -> time:
     return datetime.strptime(f'{hour:02}::{minutes:02}::{sec:02}',
                              '%H::%M::%S').time()


class Preference(AddableToDatabase):
    WEIGHT_DEFAULT = 0
    WEIGHT_SCHEDULE = 1
    WEIGHT_TEMPORARY = 2
    TTL = timedelta(minutes=20)

    def __init__(self, preference_timestamp: datetime, room_name: str, time_start: time, time_end: time, value: float, weight: int):
        self.weight: int = weight
        self.room_name: str = room_name
        self.value: float = value
        self.preference_timestamp: datetime = preference_timestamp
        self.time_start: time = time_start
        self.time_end: time = time_end

    @classmethod
    def as_default(cls, value, room_name):
        time_start = get_time(0)
        time_end = get_time(23, 59, 59)
        return cls(datetime.now(), room_name, time_start, time_end, value, cls.WEIGHT_DEFAULT)

    @classmethod
    def as_schedule(cls, value, room_name, time_start: time, time_end: time):
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
