import paho.mqtt.client as mqtt

# Define the broker parameters
broker_address = "home-automation.local"  # Replace with your Raspberry Pi's IP address
broker_port = 1883  # Default MQTT port

# If you have set up user authentication on the broker
username = "dieter"
password = "dieter"

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribe to a topic if needed
    client.subscribe("#")

# Callback function when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {str(msg.payload)}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password if authentication is required
client.username_pw_set(username, password)

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT client loop
client.loop_start()

# Publish a test message
client.publish("testTopic", "Hello, MQTT!")

# Keep the script running to receive messages
try:
    while True:
        pass
except KeyboardInterrupt:
    # Disconnect the client on keyboard interrupt
    client.disconnect()
    print("Disconnected from the broker.")
