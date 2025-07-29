import time
from machine import Pin, disable_irq, enable_irq

class DHTBase:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OPEN_DRAIN)
        self.buf = bytearray(5)

    def _send_init_signal(self):
        self.pin.init(Pin.OPEN_DRAIN)
        self.pin.value(1)
        time.sleep_ms(250)
        self.pin.value(0)
        time.sleep_ms(18)
        irq_state = disable_irq()
        self.pin.value(1)
        time.sleep_us(10)
        enable_irq(irq_state)

    def _wait_for_pin(self, target, timeout_us):
        start = time.ticks_us()
        while self.pin.value() != target:
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                return False
        return True

    def _time_pulse(self, level, timeout_us):
        start = time.ticks_us()
        while self.pin.value() != level:
            if time.ticks_diff(time.ticks_us(), start) > timeout_us:
                return -1
        begin = time.ticks_us()
        while self.pin.value() == level:
            if time.ticks_diff(time.ticks_us(), begin) > timeout_us:
                return -1
        return time.ticks_diff(time.ticks_us(), begin)

    def measure_raw(self):
        buf = self.buf
        for i in range(5):
            buf[i] = 0

        self._send_init_signal()

        irq_state = disable_irq()
        try:
            # Wait for sensor response (goes low)
            if not self._wait_for_pin(0, 100):
                raise OSError("Sensor timeout 1")

            # 80us low
            t = self._time_pulse(1, 150)
            if t < 0:
                raise OSError("Sensor timeout 2")

            # 40 bits of data
            for i in range(40):
                t = self._time_pulse(1, 100)
                if t < 0:
                    raise OSError("Sensor timeout 3")
                buf[i // 8] = (buf[i // 8] << 1) | (t > 48)
        finally:
            enable_irq(irq_state)

        return buf

# Example usage for DHT11 (could be subclassed for DHT22 with additional conversion)
class DHT11(DHTBase):
    def measure(self):
        buf = self.measure_raw()
        humidity = buf[0]
        temperature = buf[2]
        checksum = sum(buf[:4]) & 0xFF
        if checksum != buf[4]:
            raise ValueError("Checksum error")
        self.temperature = temperature
        self.humidity = humidity

    def temperature(self):
        return self.temperature

    def humidity(self):
        return self.humidity