from flask import Blueprint, jsonify, current_app
from communication import receiver, sender, constants

routes = Blueprint('routes', __name__)
broker = "localhost"

receiver_api = receiver.Receiver(broker, constants.ROOM_DATA)
sender_api = sender.Sender(broker, constants.DIRECTIVES)

@routes.route("/")
def index():
    return current_app.send_static_file("index.html")

@routes.route("/living_room/data")
def get_data_for_living_room():
    # Get data from database and return it
    list_of_records = []
    dict_to_json = {"day":[], "week":[], "month":[]}
    for rec in list_of_records:
        # check where record belongs and add it to proper label
        pass
    return jsonify(dict_to_json)

@routes.route("/kitchen/data")
def get_data_for_kitchen():
    # Get data from database and return it
    list_of_records = []
    dict_to_json = {"day":[], "week":[], "month":[]}
    for rec in list_of_records:
        # check where record belongs and add it to proper label
        pass
    return jsonify(dict_to_json)

@routes.route("/bathroom/data")
def get_data_for_bathroom():
    # Get data from database and return it
    list_of_records = []
    dict_to_json = {"day":[], "week":[], "month":[]}
    for rec in list_of_records:
        # check where record belongs and add it to proper label
        pass
    return jsonify(dict_to_json)

@routes.route("/living_room/current")
def get_current_lvr_state():
    # Get the state for the latest record
    latest_rec = []
    dict_to_json = {"temperature": 23.18, "humidity": 56.76, "pressure":1100, "thermostat_state":True, "dryer_state":False}
    return jsonify(dict_to_json)

@routes.route("/kitchen/current")
def get_current_ktch_state():
    # Get the state for the latest record
    latest_rec = []
    dict_to_json = {"temperature": 23.18, "humidity": 56.76, "pressure":1100, "thermostat_state":True, "dryer_state":False}
    return jsonify(dict_to_json)

@routes.route("/bathroom/current")
def get_current_bth_state():
    # Get the state for the latest record
    latest_rec = []
    dict_to_json = {"temperature": 23.18, "humidity": 56.76, "pressure":1100, "thermostat_state":True, "dryer_state":False}
    return jsonify(dict_to_json)

@routes.route("/living_room/aims")
def get_lvr_aims():
    def_tmp_and_hum = []
    temp_prefs = []
    hum_prefs = []
    dict_to_json = {"def_temp":24.56, "def_hum":60.45, "temp_prefs": [], "hum_prefs":[]}
    for tmp_pref_rec in temp_prefs:
        dict_to_json["temp_prefs"].append({"time_start":"9:00", "time_end":"18:00", "temp":24.7})
    for hum_pref_rec in hum_prefs:
        dict_to_json["hum_prefs"].append({"time_start":"9:00", "time_end":"18:00", "hum":65.7})
    
    return jsonify(dict_to_json)

@routes.route("/kitchen/aims")
def get_ktch_aims():
    def_tmp_and_hum = []
    temp_prefs = []
    hum_prefs = []
    dict_to_json = {"def_temp":24.56, "def_hum":60.45, "temp_prefs": [], "hum_prefs":[]}
    for tmp_pref_rec in temp_prefs:
        dict_to_json["temp_prefs"].append({"time_start":"9:00", "time_end":"18:00", "temp":24.7})
    for hum_pref_rec in hum_prefs:
        dict_to_json["hum_prefs"].append({"time_start":"9:00", "time_end":"18:00", "hum":65.7})
    
    return jsonify(dict_to_json)
    
@routes.route("/bathroom/aims")
def get_bth_aims():
    def_tmp_and_hum = []
    temp_prefs = []
    hum_prefs = []
    dict_to_json = {"def_temp":24.56, "def_hum":60.45, "temp_prefs": [], "hum_prefs":[]}
    for tmp_pref_rec in temp_prefs:
        dict_to_json["temp_prefs"].append({"time_start":"9:00", "time_end":"18:00", "temp":24.7})
    for hum_pref_rec in hum_prefs:
        dict_to_json["hum_prefs"].append({"time_start":"9:00", "time_end":"18:00", "hum":65.7})
    
    return jsonify(dict_to_json)