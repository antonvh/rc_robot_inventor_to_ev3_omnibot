#!/usr/bin/env pybricks-micropython

# Run this script on a three-wheel omnibot.
# Building instructions here: 
# https://antonsmindstorms.com/product/rubber-band-cannon-omnibot-building-instructions-pdf/

# Author: Anton's Mindstorms
# Full tutorial on https://antonsmindstorms.com
# Connection class by https://pybricks.com

from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

from math import sin, radians, pi, atan2, degrees
from spikerfcomm import SpikePrimeStreamReader

# Create the connection. Replace this with the MAC address for your SPIKE hub !!
spike = SpikePrimeStreamReader('A8:E2:C1:9B:A0:61')

three_o_clock = Motor(Port.A)
seven_o_clock = Motor(Port.C)
eleven_o_clock = Motor(Port.B)
gun = Motor(Port.D)

def deadzone(value, deadzone=5):
    if abs(value) < deadzone:
        return 0
    else:
        return value

def drive(speed, direction, turn):
    three_o_clock.run( sin(radians(90 - direction)) * speed + turn)
    seven_o_clock.run( sin(radians(210 - direction)) * speed + turn)
    eleven_o_clock.run( sin(radians(330 - direction)) * speed + turn)

direction = 0
speed = 0
turn = 0
# Now you can simply read values!
while True:
    left,_,_ = spike.acceleration()
    throttle = deadzone(spike.device("C")[1]) * -50
    turn = deadzone(spike.device("E")[1],10)   * -20
    cannon = spike.device("A")[1]             * -1

    if cannon >= 5:
        # Trigger pressed
        gun.run_angle(400, -90)

    print(left, throttle, turn, cannon)

    right = left * -1
    direction = degrees( atan2(right, throttle) )
    speed = (right ** 2 + throttle ** 2) ** 0.5

    drive(speed, direction, turn)