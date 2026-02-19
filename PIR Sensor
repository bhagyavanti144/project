import RPi.GPIO as GPIO
import time

PIR_PIN = 4  # GPIO pin connected to PIR OUT

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("PIR Sensor initializing...")
time.sleep(2)  # Give sensor time to stabilize
print("Ready to detect motion!")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
            time.sleep(1)  # Delay to avoid multiple prints
        else:
            print("No Motion")
            time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()
