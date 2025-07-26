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
sensor = DHT11(Pin(17))
light_adc = ADC(Pin(26))

ntptime.settime()
rtc = RTC()

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
    return raw  #needs to be calibrated

def format_time():
    datetime = rtc.datetime()
    hour_24 = (datetime[4] - 7) % 24  
    minute = datetime[5]
    second = datetime[6]

    #Convert 24-hour to 12-hour format
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
    show_clock = True
    last_msg_from_op = ""  

    def sub_cb(topic, msg):
        nonlocal last_msg_from_op
        if topic.decode() == "op-msg-to-agnt":
            last_msg_from_op = msg.decode()
            print("Received from operator:", last_msg_from_op)

    try:
        connect_internet("Alex's iPhone 13", password="rn6er2wm8w7k")
        client = connect_mqtt(
            "e81fdd7ce1df460f84c57b5304b4903b.s1.eu.hivemq.cloud",
            "alexL", "OOBruin456"
        )
        client.set_callback(sub_cb)
        client.subscribe("op-msg-to-agnt")
        print("Connected to MQTT broker and subscribed to op-msg-to-agnt")

        while True:
            oled.fill(0)

            if show_clock:
                t = rtc.datetime()
                oled.text("Time (PST/PDT):", 0, 10)
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

                    # Display on OLED
                    oled.text("Temp: {:.1f} F".format(temp_f), 0, 0)
                    oled.text("Humidity: {}%".format(hum), 0, 15)
                    oled.text("Light: {}".format(lumens), 0, 30)
                    if last_msg_from_op:
                        #Show last message from operator
                        oled.text(last_msg_from_op[:16], 0, 45)  
                    oled.show()

                    #Publish each measurement
                    client.publish("temp", "{:.1f}".format(temp_f))
                    client.publish("humidity", str(hum))
                    client.publish("light", str(lumens))

                    print(f"Published temp: {temp_f}, humidity: {hum}, light: {lumens}")

                except Exception as e:
                    oled.text("Sensor Error", 0, 20)
                    oled.show()
                    print("Error:", e)

                client.check_msg()  #Check for new MQTT messages
                time.sleep(2)

    except KeyboardInterrupt:
        print('Keyboard interrupt')

if __name__ == "__main__":
    main()
