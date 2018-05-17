import RPi.GPIO as GPIO
import time

# https://www.youtube.com/watch?v=ddlDgUymbxc ; https://www.youtube.com/watch?v=SGwhx1MYXUs

# pin 2 positive
# pin 6 negative
# pin 7 signal

# tell the library to use the board diagram for pins
GPIO.setmode(GPIO.BOARD)

servo_pin = 7
GPIO.setup(servo_pin, GPIO.OUT)

# pin 7, 50Hz frequency
p = GPIO.PWM(servo_pin, 50)
p.start(7.5)  # duty cycle of 7.5, could be changed to 5 or whatever

try:
    while True:
        p.ChangeDutyCycle(7.5)  # neutral, value=7.5
        time.sleep(1)

        p.ChangeDutyCycle(12.5)  # 180 degrees, value=12
        time.sleep(1)

        p.ChangeDutyCycle(2.5)  # 0 degrees,value=2
        time.sleep(1)

        # this will rotate to the neutral
        GPIO.output(servo_pin, 1)
        time.sleep(0.0015)
        GPIO.output(servo_pin, 0)

        time.sleep(2)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

# 1ms - left, 1.5 ms - neutral, 2ms - right


for i in range(0, 20):
    desiredPosition = input("Where do you want the servo? 0-180 degrees:")
    dc = 1. / 18. * (float(desiredPosition)) + 2
    p.ChangeDutyCycle(dc)
