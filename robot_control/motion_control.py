from pybricks.tools import wait

import robot_control.hardware as hardware
import config


def stop_robot():
    hardware.left_motor.stop()
    hardware.right_motor.stop()


def drive(left_speed, right_speed):
    hardware.left_motor.run(left_speed)
    hardware.right_motor.run(right_speed)


def drive_forward(speed=config.DRIVE_SPEED):
    drive(speed, speed)


def drive_backward(speed=config.DRIVE_SPEED):
    drive(-speed, -speed)


def reset_gyro(angle=0):
    hardware.gyro_sensor.reset_angle(angle)


# def drive_straight_with_gyro(speed=config.DRIVE_SPEED):
#     """
#     Drives straight using the gyro angle as correction.
#     Call reset_gyro() before starting a straight driving section.
#     """

#     angle = hardware.gyro_sensor.angle()

#     left_speed = speed + angle
#     right_speed = speed - angle

#     drive(left_speed, right_speed)

def drive_straight_with_gyro(speed=config.DRIVE_SPEED):
    angle = hardware.gyro_sensor.angle()
    correction = angle * 2

    left_speed = speed - correction
    right_speed = speed + correction

    drive(left_speed, right_speed)


# def reverse_straight_with_gyro(speed=config.DRIVE_SPEED):
#     """
#     Reverses straight using the gyro angle as correction.
#     Call reset_gyro() before starting a reversing section.
#     """

#     angle = hardware.gyro_sensor.angle()

#     left_speed = speed - angle
#     right_speed = speed + angle

#     drive(left_speed, right_speed)

def reverse_straight_with_gyro(speed=config.DRIVE_SPEED):
    angle = hardware.gyro_sensor.angle()
    correction = angle
    # correction = angle * 2


    left_speed = -speed + correction
    right_speed = -speed - correction

    drive(left_speed, right_speed)


def turn_in_place_with_gyro(angle, speed=config.TURN_SPEED):
    """
    Turns the robot by a given angle using the gyro sensor.
    Positive angle = turn right.
    Negative angle = turn left.
    """

    reset_gyro(0)

    if angle > 0:
        left_speed = speed
        right_speed = -speed
    else:
        left_speed = -speed
        right_speed = speed

    while abs(hardware.gyro_sensor.angle()) < abs(angle):
        drive(left_speed, right_speed)
        wait(config.MAIN_LOOP_WAIT_MS)

    stop_robot()
    wait(200)


def turn_in_place_with_motors(angle, speed=config.TURN_SPEED):
    """
    Turns the robot by a given angle using wheel diameter and axle track.
    Positive angle = turn right.
    Negative angle = turn left.
    """

    motor_degrees = abs(angle) * config.AXLE_TRACK_MM / config.WHEEL_DIAMETER_MM

    if angle > 0:
        left_degrees = motor_degrees
        right_degrees = -motor_degrees
    else:
        left_degrees = -motor_degrees
        right_degrees = motor_degrees

    hardware.left_motor.run_angle(speed, left_degrees, wait=False)
    hardware.right_motor.run_angle(speed, right_degrees, wait=True)

    stop_robot()
    wait(200)


def reset_drive_motors():
    hardware.left_motor.reset_angle(0)
    hardware.right_motor.reset_angle(0)


def average_motor_angle():
    return (abs(hardware.left_motor.angle()) + abs(hardware.right_motor.angle())) / 2