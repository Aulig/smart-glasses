import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)
    pinTrigger = 2 # or 3
    pinEcho = 3 # or 5

    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)

    GPIO.output(pinTrigger, GPIO.LOW)
    GPIO.output(pinTrigger, GPIO.HIGH)

    time.sleep(0.00001)
    GPIO.output(pinTrigger, GPIO.LOW)

    while GPIO.input(pinEcho) == 0:
        pulseStartTime = time.time()

    while GPIO.input(pinEcho) == 1:
        pulseEndTime = time.time()

    pulseDuration = pulseEndTime - pulseStartTime
    distance = round(pulseDuration * 17150, 2)

    print("Distance: %.2f cm" % (distance))
finally:
    GPIO.cleanup()