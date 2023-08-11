import RPi.GPIO as GPIO
import time

import requests as requests

from authentication import THINGSPEAK_WRITE_API_KEY

SPEED_OF_SOUND = 34300  # cm/s

# https://i.stack.imgur.com/yHddo.png
DISTANCE_TRIGGER_PIN = 4
DISTANCE_ECHO_PIN = 17


def measure_distance():
    try:
        GPIO.setmode(GPIO.BCM)

        # distance measurement tutorial: https://linuxhint.com/measure_distance_raspberry_pi/
        GPIO.setup(DISTANCE_TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(DISTANCE_ECHO_PIN, GPIO.IN)

        GPIO.output(DISTANCE_TRIGGER_PIN, GPIO.LOW)
        GPIO.output(DISTANCE_TRIGGER_PIN, GPIO.HIGH)

        time.sleep(0.00001)
        GPIO.output(DISTANCE_TRIGGER_PIN, GPIO.LOW)

        while GPIO.input(DISTANCE_ECHO_PIN) == 0:
            time.sleep(0.00001)

        pulse_start_time = time.time()

        while GPIO.input(DISTANCE_ECHO_PIN) == 1:
            time.sleep(0.00001)

        pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = pulse_duration * SPEED_OF_SOUND / 2

        print(f"Distance: {distance}cm")

        requests.get("https://api.thingspeak.com/update",
                     params={
                         "field1": distance,
                         "api_key": THINGSPEAK_WRITE_API_KEY}
                     )
    finally:
        GPIO.cleanup()


while True:
    measure_distance()
    # 15 seconds is the rate limit for ThingSpeak (free account)
    time.sleep(15)
