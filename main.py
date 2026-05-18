#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


import config
import robot_control.motion_control as motion_control
import robot_control.hardware as hardware
import states.line_following as line_following

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


def main():
    hardware.ev3.speaker.beep()
    line_following.follow_line_for_testing()


    while True:
        # state 1 - line following
        # line_following.follow_line()
        # wait(config.MAIN_LOOP_WAIT_MS)

        # TODO: state 2 - gap detection
        # TODO: state 3 - gap measurement
        # TODO: state 4 - classify parking type
        # TODO: state 5 - perform parking
        # TODO: state 6 - safety check
        break

    hardware.ev3.speaker.beep()


main()