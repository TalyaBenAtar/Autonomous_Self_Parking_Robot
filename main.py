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
import states.parking_spot_detection as parking_spot_detection
import states.parking as parking

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


class RobotState:
    LINE_FOLLOWING = 1
    PARKING_SPOT_DETECTION = 2
    PARKING = 3
    SAFETY_CHECK = 4


def main():
    hardware.ev3.speaker.beep()
    # line_following.follow_line_for_testing()
    # line_following.test_color_sensor()


    gap_reading_count = 0
    # line_following.prepare_line_following()
    # state = RobotState.LINE_FOLLOWING
    # print("STATE:", state)

    state = RobotState.PARKING_SPOT_DETECTION
    print("STATE:", state)

    while True:
        # STATE 1 - LINE FOLLOWING
        hardware.ev3.speaker.beep()
        if state == RobotState.LINE_FOLLOWING:
            line_following.follow_line()

            side_distance = hardware.side_ultrasonic.distance()

            print("side distance:", side_distance)

            if side_distance >= config.SIDE_DISTANCE_GAP_THRESHOLD_MM:
                gap_reading_count += 1
            else:
                gap_reading_count = 0

            if gap_reading_count >= config.GAP_START_CONFIRMATION_COUNT:

                motion_control.stop_robot()

                print("POSSIBLE PARKING GAP DETECTED")
                state = RobotState.PARKING_SPOT_DETECTION
                print("STATE:", state)
                hardware.ev3.speaker.beep()


        # STATE 2 - PARKING SPOT DETECTION
        elif state == RobotState.PARKING_SPOT_DETECTION:
            parking_type, gap_length = (
                parking_spot_detection.detect_and_classify_parking_spot()
            )

            print("Parking type:", parking_type)
            print("Gap length:", gap_length)

            if parking_type == parking_spot_detection.ParkingType.TOO_SMALL:
                print("Gap too small, searching for another gap")

                state = RobotState.PARKING_SPOT_DETECTION
                print("STATE:", state)
                wait(500)
                # print("Gap too small, returning to line following")

                # gap_reading_count = 0
                # line_following.prepare_line_following()
                # state = RobotState.LINE_FOLLOWING
                # print("STATE:", state)
                # wait(2000)

            elif parking_type == parking_spot_detection.ParkingType.UNKNOWN:
                print("No valid parking spot found, stopping safely")

                motion_control.stop_robot()
                break

            else:
                print("Valid parking spot found")
                state = RobotState.PARKING
                print("STATE:", state)
                hardware.ev3.speaker.beep()
        

        # state 3 - perform parking
        elif state == RobotState.PARKING:
            parking.perform_parking(parking_type, gap_length)
            hardware.ev3.speaker.beep()
            break

        wait(config.MAIN_LOOP_WAIT_MS)

    hardware.ev3.speaker.beep()


main()


# idea:
# i think a better solution is to detect with the color sensor 
# that we are not on th line and use the gyro to angle us back on it,
#  cause if we move off the line the color sensor wont help guide us back
#   to the line cause it doesnt know where the line is. 
#   we need to reset gyro at the start of the drive once we detect a line for that too