import time
from lib import seeed_dht

class DHT22:

    def __init__(self, channel):
        self.sensor = seeed_dht.DHT("22", channel)

    def loop_sensor(self):
        #for DHT11/DHT22
        while True:
            try:
                humi, temp = self.sensor.read()
                if humi is not None:
                    print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(self.sensor.dht_type, humi, temp))
                else:
                    print('DHT{0}, humidity & temperature: {1}'.format(self.sensor.dht_type, temp))
                time.sleep(1)
            except KeyboardInterrupt:
                break
    def read_dht_data(self):
        humi, temp = self.sensor.read()
        try:
            if humi is None and temp is None: return None, None
            if humi is None: return humi, None
            if temp is None: return None, temp
            return humi, temp
        except Exception as e:
            print(f"Error reading from sensor: {e}")
            return None
