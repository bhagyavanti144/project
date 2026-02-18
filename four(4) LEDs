import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# LED pins
led_pins = [17, 27, 22, 23]

# Setup pins as output
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        # Turn all LEDs ON
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)

        # Turn all LEDs OFF
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
