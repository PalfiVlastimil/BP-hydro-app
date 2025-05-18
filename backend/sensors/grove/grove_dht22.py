import time
import seeed_dht
import numpy as np
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
        humid, temp = self.sensor.read()
        try:
            if humid is None and temp is None: return None, None
            if humid is None: return humid, None
            if temp is None: return None, temp
            return humid, temp
        except Exception as e:
            print(f"Error reading from sensor: {e}")
            return None
    def calculate_VPD(self):
        """
            Calculates water pressure deficit
            temp: air temperature
            humid: relative humidity
            returns VPD in Pascal (Pa)
        """
        humid, temp = self.read_dht_data()
        # firstly calculate saturation vapor pressure
        es = 0.6108*np.exp((17.27*temp)/(temp+237.3))
        # then actual vapor pressure
        ea = es*(humid/100)
        result = (es - ea)*1000 # converstion from kPa to Pa
        return result


