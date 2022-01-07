/* init for all databases */

CREATE TABLE records (
record_time timestamp,
room_name text,
record_temp double,
record_humidity double,
record_press int,

device_termost boolean,
device_dryer boolean,

PRIMARY KEY (record_time)
);

CREATE TABLE preferences (
default_temp double,
default_hum double,
PRIMARY KEY ((default_temp, default_hum))
);

CREATE TABLE preferences_temp (
time_start time,
time_end time,
temp double,
PRIMARY KEY (time_start, time_end)
);

CREATE TABLE preferences_hum (
time_start time,
time_end time,
hum double,
PRIMARY KEY (time_start, time_end)
);
