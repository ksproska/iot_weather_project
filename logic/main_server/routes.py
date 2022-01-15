from database.connect import Connection
from flask import Blueprint, jsonify, current_app
from communication import receiver, sender, constants
from datetime import datetime
import json

routes = Blueprint('routes', __name__)
broker = "localhost"

receiver_api = receiver.Receiver(broker, constants.ROOM_DATA)
sender_api = sender.Sender(broker, constants.DIRECTIVES)
json_file = open("config.json")
config = json.load(json_file)

json_file.close()

list_of_rooms = config['rooms']


@routes.route("/")
def index():
    return current_app.send_static_file("index.html")

@routes.route("/roomnames")
def get_room_data():
    return jsonify(config)

@routes.route(r"/<room_identifier>/data")
def get_data_for_room(room_identifier):
    # Get data from database
    db_connection = Connection()
    list_of_records = db_connection.get_all_records(room_identifier)
    dict_to_json = {"day":[], "week":[], "month":[]}
    for rec in list_of_records:

        # Check where record belongs and add it to proper label

        if (datetime.now() - rec.record_time).days < 1:
            dict_to_json["day"].append({"year":rec.record_time.year,"month":rec.record_time.month, "day": rec.record_time.day, "hour":rec.record_time.hour, "minute":rec.record_time.minute,"second":rec.record_time.second, "temperature": rec.record_temp, "humidity": rec.record_humidity, "pressure":rec.record_press, "thermostat_state":rec.device_termost, "dryer_state":rec.device_dryer})
        if (datetime.now() - rec.record_time).days < datetime.today().weekday():
            dict_to_json["week"].append({"year":rec.record_time.year,"month":rec.record_time.month, "day": rec.record_time.day, "hour":rec.record_time.hour, "minute":rec.record_time.minute,"second":rec.record_time.second, "temperature": rec.record_temp, "humidity": rec.record_humidity, "pressure":rec.record_press, "thermostat_state":rec.device_termost, "dryer_state":rec.device_dryer})
        if (datetime.now() - rec.record_time).days < rec.record_time.day:
            dict_to_json["month"].append({"year":rec.record_time.year,"month":rec.record_time.month, "day": rec.record_time.day, "hour":rec.record_time.hour, "minute":rec.record_time.minute,"second":rec.record_time.second, "temperature": rec.record_temp, "humidity": rec.record_humidity, "pressure":rec.record_press, "thermostat_state":rec.device_termost, "dryer_state":rec.device_dryer})
    db_connection.close()
    return jsonify(dict_to_json)

@routes.route(r"/<room_identifier>/current")
def get_current_room_state(room_identifier):

    # Get the state for the latest record
    db_connection = Connection()

    latest_rec = db_connection.get_all_records(room_identifier)[-1]
    dict_to_json = {"year":latest_rec.record_time.year,"month":latest_rec.record_time.month, "day": latest_rec.record_time.day, "hour":latest_rec.record_time.hour, "minute":latest_rec.record_time.minute,"second":latest_rec.record_time.second, "temperature": latest_rec.record_temp, "humidity": latest_rec.record_humidity, "pressure":latest_rec.record_press, "thermostat_state":latest_rec.device_termost, "dryer_state":latest_rec.device_dryer}
    db_connection.close()
    return jsonify(dict_to_json)


@routes.route(r"/<room_identifier>/aims")
def get_room_aims(room_identifier):
    db_connection = Connection()

    temp_prefs = db_connection.get_all_scheduled_preferences_temperature(room_identifier)
    hum_prefs = db_connection.get_all_scheduled_preferences_humidity(room_identifier)
    dict_to_json = {"def_temp":db_connection.default_preference_temperature(room_identifier), "def_hum":db_connection.default_preference_humidity(room_identifier), "temp_prefs": [], "hum_prefs":[]}
    for tmp_pref_rec in temp_prefs:
        dict_to_json["temp_prefs"].append({"time_start":str(tmp_pref_rec.time_start)[0:-3], "time_end":str(tmp_pref_rec.time_end)[0:-3], "temp":tmp_pref_rec.value})
    for hum_pref_rec in hum_prefs:
        dict_to_json["temp_prefs"].append({"time_start":str(hum_pref_rec.time_start)[0:-3], "time_end":str(hum_pref_rec.time_end)[0:-3], "temp":hum_pref_rec.value})
    
    db_connection.close()
    return jsonify(dict_to_json)

@routes.route(r"/<room_identifier>/set_def_hum")
def set_default_humidity(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

@routes.route(r"/<room_identifier>/set_def_temp")
def set_default_temperature(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

@routes.route(r"/<room_identifier>/delete_temp_schedule")
def delete_temp_schedule(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

@routes.route(r"/<room_identifier>/delete_hum_schedule")
def delete_hum_schedule(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

@routes.route(r"/<room_identifier>/add_temp_schedule")
def add_temp_schedule(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

@routes.route(r"/<room_identifier>/add_hum_schedule")
def add_hum_schedule(room_identifier):
    db_connection = Connection()
    db_connection.close()
    pass

