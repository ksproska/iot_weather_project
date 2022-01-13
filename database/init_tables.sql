CREATE TABLE IF NOT EXISTS record (
    record_time timestamp,
    room_name text,
    record_temp double,
    record_humidity double,
    record_press int,

    device_termost boolean,
    device_dryer boolean,

    PRIMARY KEY (room_name, record_time)
);


CREATE TABLE IF NOT EXISTS preference_temperature (
    preference_timestamp timestamp,
    time_start time,
    time_end time,
    value double,
    weight int,
    room_name text,
    PRIMARY KEY (room_name, weight, preference_timestamp)
);


CREATE TABLE IF NOT EXISTS preference_humidity (
    preference_timestamp timestamp,
    time_start time,
    time_end time,
    value double,
    weight int,
    room_name text,
    PRIMARY KEY (room_name, weight, preference_timestamp)
);