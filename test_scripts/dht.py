import dht
import machine
import utime

# Define the DHT11 sensor pin
dht_pin = machine.Pin(21)  # Change this to the GPIO pin connected to the DHT11 sensor

# Create a DHT object
dht_sensor = dht.DHT11(dht_pin)

while True:
    try:
        # Read sensor data
        dht_sensor.measure()
        temperature_celsius = dht_sensor.temperature()
        humidity_percentage = dht_sensor.humidity()

        # Print the sensor data
        print("Temperature: {:.1f}°C, Humidity: {:.1f}%".format(temperature_celsius, humidity_percentage))

    except Exception as e:
        print("Error reading DHT11:", e)

    # Wait for a few seconds before reading again
    utime.sleep(10)
