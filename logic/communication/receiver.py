import paho.mqtt.client as mqtt


class Receiver:
    def __init__(self, broker, identifier):
        self.broker = broker
        self.identifier = identifier
        self.client = mqtt.Client()
        self.client.username_pw_set(username='tech_user', password='1234')

        # TLS encryption settings, commented out because hamachi VPN is in use

        # self.client.tls_set('ca.crt')
        # self.client.tls_insecure_set(True)


    def connect_to_broker(self):
        self.client.connect(self.broker)

    def disconnect_from_broker(self):
        self.client.disconnect(self.broker)

    def subscribe(self):
        self.client.subscribe(self.identifier)

    def loop_start(self):
        self.client.loop_start()



