import sys

sys.path.append('/home/pi/Desktop/proj/iot_weather_project')
from database.tables_as_classes import Preference_humidity, Preference_temperature, Record
from flask import Flask
from routes import routes, sender_api, receiver_api
from database.connect import Connection
import threading

app = Flask(__name__)
app.register_blueprint(routes)

sender_api.connect_to_broker()


def process_message(client, userdata, message):
    # Split message to get required information about room, temp and humidity
    connection = Connection()
    message_decoded = str(message.payload.decode("utf-8")).split("#")
    if len(message_decoded) == 4:
        room_id = message_decoded[0]
        print(message_decoded)
        temperature = float(message_decoded[1])
        humidity = float(message_decoded[2])
        pressure = int(message_decoded[3])

        # Get informations from database about current preferences
        current_pref_temp = connection.current_preference_temperature(room_id)
        current_pref_hum = connection.current_preference_humidity(room_id)

        # Save records to database
        connection.add_object(Record.with_current_time(room_id, temperature, humidity, pressure, current_pref_temp > temperature, current_pref_hum < humidity))

        is_thermostat_on = "true" if current_pref_temp > temperature else "false"
        is_dryer_on = "true" if current_pref_hum < humidity else "false"

        # If temperature is too low, send message that thermostat should be on
        # If humidity is too high, send message that dryer should be on

        sender_api.publish(f"{room_id}#{is_thermostat_on}#{is_dryer_on}")
    elif len(message_decoded) == 3:
        room_id = message_decoded[0]
        op_code = message_decoded[1]
        value = float(message_decoded[2])
        if op_code == "THERM":
            connection.add_object(Preference_temperature.as_temporary(value,room_id))
        elif op_code == "DRY":
            connection.add_object(Preference_humidity.as_temporary(value,room_id))
    connection.close()
    pass

def run_receiver():
    receiver_api.connect_to_broker()
    receiver_api.client.on_message = process_message
    receiver_api.loop_start()
    receiver_api.subscribe()


rec_thread = threading.Thread(target=run_receiver)
rec_thread.start()
