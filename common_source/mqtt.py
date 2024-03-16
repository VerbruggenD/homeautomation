# imports
from umqtt.simple import MQTTClient

class MQTT:
    def __init__(self, client_id, server, port, user, password, keepalive=7200, ssl=False, ssl_params=None):
        self.client_id = client_id
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params

        self.client = None

    def connect(self):
        self.client = MQTTClient(client_id=self.client_id,
                                 server=self.server,
                                 port=self.port,
                                 user=self.user,
                                 password=self.password,
                                 keepalive=self.keepalive,
                                 ssl=self.ssl,
                                 ssl_params=self.ssl_params)
        self.client.connect()

    def publish(self, topic, value):
        if not self.client:
            raise RuntimeError("MQTT client not connected. Call connect() method first.")
        self.client.publish(topic, value)
        print("Published: " + topic + " " + value)
