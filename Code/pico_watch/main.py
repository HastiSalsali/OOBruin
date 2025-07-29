from connections import connect_mqtt, connect_internet
import time
from time import sleep
from machine import Pin, I2C, ADC, RTC
import ssd1306
from dht import DHT11
import ujson
import ntptime

#Setup I2C on pins 0 (SDA) and 1 (SCL) with 400kHz frequency
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

#Initialize the OLED display using I2C
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#Initialize DHT11 sensor on GPIO pin 16
sensor = DHT11(Pin(16))

#Initialize analog light sensor connected to ADC pin 26
light_adc = ADC(Pin(26))

#Initialize real-time clock
rtc = RTC()


#Calibration values:
#adc_val = adc_dark when lumens = 0
#adc_val = adc_bright when lumens = 1
adc_dark = 4849
adc_bright = 63823

#Using a linear model for light sensor: lumens = m(adc_val) + b
#Calculating m and b from the calibration values
m = 1 / (adc_bright - adc_dark)
b = -m * adc_dark

#Function to read light sensor value and convert to lumens
def read_light_lumens():
    raw = light_adc.read_u16()
    lumens = m * raw + b
    return max(0, lumens)

#Function to format current RTC time into 12-hour clock string
def format_time():
    
    #Retrieve the current date and time from Pico's clock
    #Ex: (year, month, day, weekday, hour, minute, second, subseconds)
    datetime = rtc.datetime() 
    hour_24 = (datetime[4] - 7) % 24  #Adjust the 5th element (hour) to display PST
    minute = datetime[5]
    second = datetime[6]
    
    #Convert 24-hour to 12-hour format with AM/PM
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

#Main function controlling sensor reading, display, and MQTT messaging
def main():
    show_clock = False #Flag to switch display between clock and sensor data
    last_msg_from_op = "" #Store last message received from MQTT operator

    #MQTT message callback function
    def cb(topic, msg):
        nonlocal show_clock, last_msg_from_op
        if topic == b"display":
            last_msg_from_op = msg.decode() #Decode and save message from operator
            print("Received from operator:", last_msg_from_op)
            
            return last_msg_from_op
            
        elif topic == b"clock-setting":
            msg_str = msg.decode()
            show_clock = (msg_str.lower() == "true") #Check if it equals "true", boolean is case-sensitive

    try:
        #Connect to Wi-Fi
        connect_internet("bruins", password="connect12")

        #Sync the device's real-time clock (RTC) using the internet
        try:
            ntptime.host = "time.google.com"
            ntptime.settime()
            print("Time synced via NTP")
        except Exception as e:
            print("Failed to sync time:", e)

        #Connect to MQTT broker with username and password
        client = connect_mqtt(
            "e81fdd7ce1df460f84c57b5304b4903b.s1.eu.hivemq.cloud",
            "alexL", "OOBruin456"
        )
        #Set the MQTT callback function
        client.set_callback(cb)
        #Subscribe to topics to receive messages
        client.subscribe("display")
        client.subscribe("clock-setting")
        print("subscribed to display & clock-setting")

        while True:
            oled.fill(0) #Clear OLED display

            if show_clock:
                #Show current time
                oled.text("Time (PST):", 0, 10)
                oled.text(format_time(), 0, 30)
                oled.show()
                time.sleep(1)

            else:
                try:
                    #Measure temperature and humidity from DHT11
                    sensor.measure()
                    temp_c = sensor.temperature
                    
                    #Convert Celsius to Fahrenheit, adjust by -2 (calibration offset)
                    temp_f = temp_c * 9 / 5 + 32 - 8.5
                    hum = sensor.humidity
                    
                    #Read calibrated light sensor value
                    lumens = read_light_lumens()
                    
                    #Display sensor values on OLED
                    oled.text("Temp: {:.1f} F".format(temp_f), 0, 0)
                    oled.text("Humidity: {}%".format(hum), 0, 13)
                    oled.text("Light: {}".format(lumens), 0, 26)
                    
                    #Display last operator message if present
                    if last_msg_from_op:
                        oled.text(last_msg_from_op[:16], 0, 40)
                        oled.text(last_msg_from_op[16:32], 0, 53)


                    oled.show()
                    
                    #Publish sensor data to MQTT topics
                    client.publish("temp", "{:.1f}".format(temp_f))
                    client.publish("humidity", str(hum))
                    client.publish("light", str(lumens))

                    print(f"Published temp: {temp_f}, humidity: {hum}, light: {lumens}")

                except Exception as e:
                    print("Sensor Error:", e)
                
                #Check for new MQTT messages
                client.check_msg()
                time.sleep(5)

    except KeyboardInterrupt:
        print('Keyboard interrupt')

#Run main() if this file is ran directly
if __name__ == "__main__":
    main()