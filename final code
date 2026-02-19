import Adafruit_DHT
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
from time import sleep

# --- Sensor setup ---
DHT_SENSOR = Adafruit_DHT.DHT11   # change to DHT22 if using it
DHT_PIN = 4  # GPIO4

# --- Fan setup ---
FAN_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# --- LCD setup ---
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            lcd.clear()
            
            # Display values
            lcd.write_string(f"Temp:{temperature}C")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Hum:{humidity}%")

            # Fan control
            if temperature >= 30:   # set your threshold
                GPIO.output(FAN_PIN, GPIO.HIGH)
            else:
                GPIO.output(FAN_PIN, GPIO.LOW)

        else:
            lcd.clear()
            lcd.write_string("Sensor error")

        sleep(2)

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
