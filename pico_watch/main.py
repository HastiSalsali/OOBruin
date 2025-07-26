from connections import connect_mqtt, connect_internet
import time
from time import sleep
from machine import Pin, I2C, ADC, RTC
import ssd1306
from dht import DHT11


def main():
    try:
        connect_internet("",password="") #ssid (wifi name), pass
        client = connect_mqtt("", "", "") # url, user, pass

        while True:
            client.check_msg()
            sleep(0.1)

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

sensor = DHT11(Pin(17))
light_adc = ADC(Pin(26))

rtc = RTC()
rtc.datetime((2025, 7, 25, 4, 14, 10, 0, 0))

show_clock = False

# Calibration values
#adc_dark =      #ADC when it's dark
#adc_bright =   #ADC under known bright light (e.g., 1 lumen)

#Compute slope and intercept for y = mx + b
#m = 1 / (adc_bright - adc_dark)
#b = -m * adc_dark

def read_light_lumens():
    raw = light_adc.read_u16()
    #lumens = m * raw + b
    #return max(0, lumens)
    return raw

def format_time(t):
    hour = t[4]
    minute = t[5]
    second = t[6]
    return "{:02d}:{:02d}:{:02d}".format(hour, minute, second)

while True:
    oled.fill(0)

    if show_clock:
        t = rtc.datetime()
        oled.text("Time (PST/PDT):", 0, 10)
        oled.text(format_time(t), 0, 30)
        oled.show()
        time.sleep(1)

    else:
        try:
            sensor.measure()
            temp_c = sensor.temperature
            temp_f = temp_c * 9 / 5 + 32 - 2  # adjust offset if needed
            hum = sensor.humidity
            lumens = read_light_lumens()

            oled.text("Temp: {:.1f} F".format(temp_f), 0, 0)
            oled.text("Humidity: {}%".format(hum), 0, 15)
            oled.text("Light: {}".format(lumens), 0, 30)
            oled.show()

        except Exception as e:
            oled.text("Sensor Error", 0, 20)
            oled.show()

        time.sleep(2)

