from flask import Flask
from communication import receiver, sender
import threading

broker = "localhost"

receiver_api = receiver.Receiver(broker)
sender_api = sender.Sender()

def wait_for_connections():

app = Flask(__name__)


