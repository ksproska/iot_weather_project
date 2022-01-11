from flask import Flask
from communication import receiver, sender, constants
import threading


broker = "localhost"

receiver_api = receiver.Receiver(broker, constants.ROOM_DATA)
sender_api = sender.Sender(broker, constants.DIRECTIVES)
def process_message(client, userdata, message):
    print(client + " send message " + message)

def run_receiver():
    receiver_api.connect_to_broker()
    receiver_api.client.on_message = process_message
    receiver_api.loop_start()
    receiver_api.subscribe()


rec_thread = threading.Thread(target=run_receiver, )
rec_thread.start()

app = Flask(__name__)


