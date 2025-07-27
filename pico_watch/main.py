from connections import connect_mqtt, connect_internet
import time
from time import sleep
from machine import Pin, I2C, ADC, RTC
import ssd1306
from dht import DHT11
import ujson
import ntptime

# Setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor = DHT11(Pin(13))
light_adc = ADC(Pin(26))
rtc = RTC()

# Calibration values (not used yet)
#adc_dark = ...
#adc_bright = ...
#m = 1 / (adc_bright - adc_dark)
#b = -m * adc_dark

def read_light_lumens():
    raw = light_adc.read_u16()
    #lumens = m * raw + b
    #return max(0, lumens)
    return raw  # needs to be calibrated

def format_time():
    datetime = rtc.datetime()
    hour_24 = (datetime[4] - 7) % 24  # Adjust for PDT/PST offset
    minute = datetime[5]
    second = datetime[6]

    if hour_24 == 0:
        hour_12 = 12
        am_pm = "AM"
    elif 1 <= hour_24 < 12:
        hour_12 = hour_24
        am_pm = "AM"
    elif hour_24 == 12:
        hour_12 = 12
        am_pm = "PM"
    else:
        hour_12 = hour_24 - 12
        am_pm = "PM"

    return "{:2d}:{:02d}:{:02d} {}".format(hour_12, minute, second, am_pm)

def main():
    show_clock = False
    last_msg_from_op = ""

    def cb(topic, msg):
        nonlocal show_clock, last_msg_from_op
        if topic == b"display":
            last_msg_from_op = msg.decode()
            print("Received from operator:", last_msg_from_op)
            
            #oled.text("Msg:", 0, 45)
            #oled.text(last_msg_from_op[:16], 0, 60)
            #oled.show()
            #time.sleep(10)  #briefly show the message
            return last_msg_from_op
            
        elif topic == b"clock-setting":
            show_clock = (msg_str.lower() == "true")

    try:
        #Connect to Wi-Fi
        connect_internet("bruins", password="connect12")

        try:
            ntptime.host = "time.google.com"
            ntptime.settime()
            print("Time synced via NTP")
        except Exception as e:
            print("Failed to sync time:", e)

        #Set up MQTT
        client = connect_mqtt(
            "e81fdd7ce1df460f84c57b5304b4903b.s1.eu.hivemq.cloud",
            "alexL", "OOBruin456"
        )
        client.set_callback(cb)
        client.subscribe("display")
        client.subscribe("clock-setting")
        print("subscribed to display & clock-setting")

        while True:
            oled.fill(0)

            if show_clock:
                oled.text("Time (PST):", 0, 10)
                oled.text(format_time(), 0, 30)
                oled.show()
                time.sleep(1)

            else:
                try:
                    sensor.measure()
                    temp_c = sensor.temperature
                    temp_f = temp_c * 9 / 5 + 32 - 2
                    hum = sensor.humidity
                    lumens = read_light_lumens()

                    oled.text("Temp: {:.1f} F".format(temp_f), 0, 0)
                    oled.text("Humidity: {}%".format(hum), 0, 13)
                    oled.text("Light: {}".format(lumens), 0, 26)

                    if last_msg_from_op:
                        oled.text(last_msg_from_op[:16], 0, 40)
                        oled.text(last_msg_from_op[16:32], 0, 53)


                    oled.show()

                    client.publish("temp", "{:.1f}".format(temp_f))
                    client.publish("humidity", str(hum))
                    client.publish("light", str(lumens))

                    print(f"Published temp: {temp_f}, humidity: {hum}, light: {lumens}")

                except Exception as e:
                    print("Sensor Error:", e)

                client.check_msg()
                time.sleep(5)

    except KeyboardInterrupt:
        print('Keyboard interrupt')

if __name__ == "__main__":
    main()