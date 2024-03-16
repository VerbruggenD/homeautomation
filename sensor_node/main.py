# imports
from common_source.wifi import Wifi as wifi
from common_source.mqtt import MQTT as mqtt
from common_source import configuration as config

import machine
import dht

# Define the DHT11 sensor pin
dht_pin = machine.Pin(21)  # Change this to the GPIO pin connected to the DHT11 sensor

# Create a DHT object
dht_sensor = dht.DHT11(dht_pin)

wifi(config.wifi_ssid, config.wifi_password)
wifi.connect

mqtt(client_id=b"kudzai_raspberrypi_picow",
        server=b"6074b804f6ce45bd98dc38414f70d522.s2.eu.hivemq.cloud",
        port=8883,
        user=b"test_user",
        password=b"Dit_is_w8woord",
        keepalive=7200
    )

mqtt.connect()