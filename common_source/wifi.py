# imports
import network
import utime

class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('Waiting for connection...')
            utime.sleep(1)

        # Handle connection error
        if self.wlan.status() != 3:
            raise RuntimeError('WiFi connection failed')
        else:
            print('Connected')
            status = self.wlan.ifconfig()
            print('IP:', status[0])