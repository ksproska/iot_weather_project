import sys
sys.path.append('/home/pi/Desktop/proj/iot_weather_project')
from flask import Flask
from routes import routes, sender_api, receiver_api
import threading


sender_api.connect_to_broker()

def process_message(client, userdata, message):
    # 1. split message to get required information about room, temp and humidity
    # 2. save records to database
    pass

def run_receiver():
    receiver_api.connect_to_broker()
    receiver_api.client.on_message = process_message
    receiver_api.loop_start()
    receiver_api.subscribe()


rec_thread = threading.Thread(target=run_receiver)
rec_thread.start()

app = Flask(__name__)
app.register_blueprint(routes)

