import paho.mqtt.client as mqtt


class Receiver:
    def __init__(self, broker, identifier):
        self.broker = broker
        self.identifier = identifier
        self.client = mqtt.Client()

    def connect_to_broker(self):
        self.client.connect(self.broker)

    def disconnect_from_broker(self):
        self.client.disconnect(self.broker)

    def subscribe(self):
        self.client.subscribe(self.identifier)

    def loop_start(self):
        self.client.loop_start()


