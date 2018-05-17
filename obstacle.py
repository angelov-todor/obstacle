import RPi.GPIO as GPIO  # Import GPIO library
# Import time library
import time
from flask import Flask, request

app = Flask('my first app', static_url_path='/static')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # programming the GPIO by BCM pin numbers

# https://circuitdigest.com/microcontroller-projects/raspberry-pi-obstacle-avoiding-robot

TRIG = 17
ECHO = 27
led = 22

m11 = 16
m12 = 12
m21 = 21
m22 = 20

GPIO.setup(TRIG, GPIO.OUT)  # initialize GPIO Pin as outputs
GPIO.setup(ECHO, GPIO.IN)  # initialize GPIO Pin as input
GPIO.setup(led, GPIO.OUT)

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

GPIO.output(led, 1)

time.sleep(5)


def stop():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("stop")


def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("forward")


def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print("back")


def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("left")


def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("right")


def run():
    count = 0
    while True:
        i = 0
        avgDistance = 0
        for i in range(5):
            GPIO.output(TRIG, False)  # Set TRIG as LOW
            time.sleep(0.1)  # Delay

            GPIO.output(TRIG, True)  # Set TRIG as HIGH
            time.sleep(0.00001)  # Delay of 0.00001 seconds
            GPIO.output(TRIG, False)  # Set TRIG as LOW

            while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
                GPIO.output(led, False)
            pulse_start = time.time()

            while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
                GPIO.output(led, False)
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

            distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
            distance = round(distance, 2)  # Round to two decimal points
            avgDistance = avgDistance + distance

        avgDistance = avgDistance / 5
        print(avgDistance)

        flag = 0
        if avgDistance < 15:  # Check whether the distance is within 15 cm range
            count = count + 1
            stop()
            time.sleep(1)
            back()
            time.sleep(1.5)
            if (count % 3 == 1) & (flag == 0):
                right()
                flag = 1
            else:
                left()
                flag = 0
            time.sleep(1.5)
            stop()
            time.sleep(1)
        else:
            forward()
            flag = 0


@app.route('/forward')
def go_forward():
    forward()
    return 'forward'


@app.route('/left')
def go_left():
    left()
    return 'left'


@app.route('/right')
def go_right():
    right()
    return 'right'


@app.route('/stop')
def do_stop():
    stop()
    return 'stop'


@app.route('/back')
def go_back():
    back()
    return 'back'


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    stop()
    app.run(host='0.0.0.0')
