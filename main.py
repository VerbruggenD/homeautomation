import network
import utime
import machine
from umqtt.simple import MQTTClient
import dht

# Define the DHT11 sensor pin
dht_pin = machine.Pin(21)  # Change this to the GPIO pin connected to the DHT11 sensor

# Create a DHT object
dht_sensor = dht.DHT11(dht_pin)

# Define your Wi-Fi credentials
wifi_ssid = "telenet-E7B89D9"
wifi_password = "uMznf7kxuTch"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

#Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

def connectMQTT():
    client = MQTTClient(client_id=b"kudzai_raspberrypi_picow",
        server=b"6074b804f6ce45bd98dc38414f70d522.s2.eu.hivemq.cloud",
        port=8883,
        user=b"test_user",
        password=b"Dit_is_w8woord",
        keepalive=7200,
        ssl=True,
        ssl_params={'server_hostname':'6074b804f6ce45bd98dc38414f70d522.s2.eu.hivemq.cloud'}
    )

    client.connect()
    return client

client = connectMQTT()

def publish(topic, value):
    client.publish(topic, value)
    print("Published: " + topic + " " + value)

while True:
    try:
        # Read sensor data
        dht_sensor.measure()
        temperature_celsius = dht_sensor.temperature()
        humidity_percentage = dht_sensor.humidity()

        # Print the sensor data
        print("Temperature: {:.1f}°C, Humidity: {:.1f}%".format(temperature_celsius, humidity_percentage))

        #publish as MQTT payload
        publish('room/dieter/temp', "{:.1f}".format(temperature_celsius))
        publish('room/dieter/humid', "{:.1f}".format(humidity_percentage))

    except Exception as e:
        print("Error reading DHT11:", e)
    #delay 5 seconds
    utime.sleep(60)