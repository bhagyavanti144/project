import RPi.GPIO as GPIO
import time

# 4-way traffic light pin mapping
signals = {
    "North": {"red": 7, "yellow": 10, "green": 11},
    "East":  {"red": 12, "yellow": 13, "green": 15},
    "South": {"red": 16, "yellow": 18, "green": 19},
    "West":  {"red": 21, "yellow": 22, "green": 23}
}

# GPIO setup
GPIO.setmode(GPIO.BOARD)  # using physical pin numbering
for direction in signals:
    for pin in signals[direction].values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def set_signal(active_direction):
    """Turn green for one direction and red for others"""
    for direction, lights in signals.items():
        if direction == active_direction:
            GPIO.output(lights["red"], GPIO.LOW)
            GPIO.output(lights["yellow"], GPIO.LOW)
            GPIO.output(lights["green"], GPIO.HIGH)
        else:
            GPIO.output(lights["green"], GPIO.LOW)
            GPIO.output(lights["yellow"], GPIO.LOW)
            GPIO.output(lights["red"], GPIO.HIGH)

try:
    while True:
        for direction in signals.keys():
            print(f"🚦 Traffic open for {direction}")

            # Green ON for current direction
            set_signal(direction)
            time.sleep(5)

            # Yellow ON before red
            GPIO.output(signals[direction]["green"], GPIO.LOW)
            GPIO.output(signals[direction]["yellow"], GPIO.HIGH)
            time.sleep(2)
            GPIO.output(signals[direction]["yellow"], GPIO.LOW)

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    GPIO.cleanup()
    print("GPIO cleanup done")
