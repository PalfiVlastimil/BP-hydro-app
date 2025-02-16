import smbus2
import time

class GroveWaterLevelSensor:
    NO_TOUCH          = 0xFE
    ATTINY1_HIGH_ADDR = 0x78
    THRESHOLD         = 100
    ATTINY2_LOW_ADDR  = 0x77
    SENSORVALUE_MIN   = 250
    SENSORVALUE_MAX   = 255

    def __init__(self, channel):
        self.bus = smbus2.SMBus(channel)

    def read_percentage(self):
        low_data = [0] * 8
        high_data = [0] * 12
        low_count = 0
        high_count = 0
        touch_val = 0
        trig_section = 0

        try:
            self.bus.write_byte(self.ATTINY2_LOW_ADDR, 0)
            low_data = list(self.bus.read_i2c_block_data(self.ATTINY2_LOW_ADDR, 0, 8))

            self.bus.write_byte(self.ATTINY1_HIGH_ADDR, 0)
            high_data = list(self.bus.read_i2c_block_data(self.ATTINY1_HIGH_ADDR, 0, 12))
            
            time.sleep(0.01)
            
            for i in range(8):
                if self.SENSORVALUE_MIN <= low_data[i] <= self.SENSORVALUE_MAX:
                    low_count += 1

            for i in range(12):
                if self.SENSORVALUE_MIN <= high_data[i] <= self.SENSORVALUE_MAX:
                    high_count += 1

            for i in range(8):
                if low_data[i] > self.THRESHOLD:
                    touch_val |= 1 << i

            for i in range(12):
                if high_data[i] > self.THRESHOLD:
                    touch_val |= (1 << (8 + i))

            while touch_val & 0x01:
                trig_section += 1
                touch_val >>= 1
            
            # Convert to percentage
            return (trig_section * 5)
        except Exception as e:
            print(f"Error reading from sensor: {e}")
            return None

    def loop_sensor(self, start=True):
        while start:
            try:
                level_percent = self.read_percentage()
                if level_percent is not None:
                    print(f"Hladina vody: {level_percent:.1f}%")
                time.sleep(1)
            except KeyboardInterrupt:
                break
