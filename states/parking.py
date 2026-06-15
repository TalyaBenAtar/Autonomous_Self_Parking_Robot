from pybricks.tools import wait

import config
import robot_control.hardware as hardware
import robot_control.motion_control as motion_control
from states.parking_spot_detection import ParkingType


def read_side_distance():
    return hardware.side_ultrasonic.distance()


def read_rear_distance():
    return hardware.rear_ultrasonic.distance()


def is_rear_safe():
    return read_rear_distance() > config.MIN_REAR_DISTANCE_MM


def stop_if_too_close():
    if not is_rear_safe():
        motion_control.stop_robot()
        print("STOP: rear obstacle too close")
        return True

    return False


def calculate_side_correction(target_side_distance):
    """
    Positive correction means robot is too far from the right side.
    Negative correction means robot is too close to the right side.
    """

    side_distance = read_filtered_side_distance()
    error = side_distance - target_side_distance
    correction = error * config.PARKING_SIDE_KP

    if correction > config.MAX_PARKING_CORRECTION:
        correction = config.MAX_PARKING_CORRECTION

    if correction < -config.MAX_PARKING_CORRECTION:
        correction = -config.MAX_PARKING_CORRECTION

    return correction


def read_filtered_rear_distance():
    total = 0

    for _ in range(config.ULTRASONIC_FILTER_SAMPLES):
        total += read_rear_distance()
        wait(config.ULTRASONIC_FILTER_WAIT_MS)

    return total / config.ULTRASONIC_FILTER_SAMPLES


def read_filtered_side_distance():
    total = 0

    for _ in range(config.ULTRASONIC_FILTER_SAMPLES):
        total += read_side_distance()
        wait(config.ULTRASONIC_FILTER_WAIT_MS)

    return total / config.ULTRASONIC_FILTER_SAMPLES


def reverse_with_side_alignment(target_side_distance, speed=config.PARKING_SPEED):
    """
    Reverses while keeping a target distance from the right side.
    Also uses the rear ultrasonic as collision protection.
    """

    if stop_if_too_close():
        return

    correction = calculate_side_correction(target_side_distance)

    left_speed = -speed + correction
    right_speed = -speed - correction

    motion_control.drive(left_speed, right_speed)

    print(
        "side:", read_filtered_side_distance(),
        "rear:", read_filtered_rear_distance(),
        "correction:", correction
    )


def reverse_until_rear_distance_with_side_alignment(
    rear_target_distance,
    side_target_distance,
    max_motor_angle,
    speed=config.PARKING_SPEED
):
    motion_control.reset_drive_motors()
    motion_control.reset_gyro()

    while (
        read_filtered_rear_distance() > rear_target_distance
        and motion_control.average_motor_angle() < max_motor_angle
    ):
        if stop_if_too_close():
            return False

        reverse_with_side_alignment(side_target_distance, speed)
        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()

    if motion_control.average_motor_angle() >= max_motor_angle:
        print("STOP: reverse max motor angle reached")
        return False

    return True


def reverse_straight_until_rear_distance(
    rear_target_distance,
    max_motor_angle,
    speed=config.PARKING_SPEED
):
    motion_control.reset_drive_motors()
    motion_control.reset_gyro()

    while (
        read_filtered_rear_distance() > rear_target_distance
        and motion_control.average_motor_angle() < max_motor_angle
    ):
        if stop_if_too_close():
            return False

        motion_control.reverse_straight_with_gyro(speed)

        print(
            "rear:", read_filtered_rear_distance(),
            "gyro:", hardware.gyro_sensor.angle(),
            "motor:", motion_control.average_motor_angle()
        )

        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()

    if motion_control.average_motor_angle() >= max_motor_angle:
        print("STOP: reverse max motor angle reached")
        return False

    return True


def drive_forward_for_motor_angle(target_angle, speed=config.PARKING_SPEED):
    if target_angle > config.MAX_FORWARD_ENTRY_ANGLE:
        target_angle = config.MAX_FORWARD_ENTRY_ANGLE

    motion_control.reset_drive_motors()
    motion_control.reset_gyro()

    while motion_control.average_motor_angle() < target_angle:
        motion_control.drive_straight_with_gyro(speed)

        print("forward motor:", motion_control.average_motor_angle())

        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()


# def final_safety_check():
#     rear_distance = read_filtered_rear_distance()
#     side_distance = read_filtered_side_distance()

#     print("Final rear distance:", rear_distance)
#     print("Final side distance:", side_distance)

#     if rear_distance <= config.MIN_REAR_DISTANCE_MM:
#         print("WARNING: rear is close, but parking completed")

#     if side_distance <= config.MIN_SIDE_DISTANCE_MM:
#         print("WARNING: side is close, but parking completed")

#     print("Parking completed successfully")
#     return True


def perform_parking(parking_type, gap_length):
    if parking_type == ParkingType.VERTICAL:
        return perform_vertical_parking(gap_length)

    if parking_type == ParkingType.PARALLEL:
        return perform_parallel_parking(gap_length)

    motion_control.stop_robot()
    print("Cannot park. Parking type:", parking_type)
    return False


def perform_vertical_parking(gap_length):
    """
    Vertical parking:
    1. Move slightly forward to align with the spot.
    2. Turn 90 degrees into the spot.
    3. Reverse straight using gyro.
    4. Stop using rear ultrasonic.
    5. Safety check.
    """

    hardware.ev3.speaker.beep()
    print("Performing vertical parking")

    drive_forward_for_motor_angle(config.VERTICAL_ENTRY_FORWARD_ANGLE)

    motion_control.turn_in_place_with_gyro(90)

    success = reverse_straight_until_rear_distance(
        config.VERTICAL_PARKING_REAR_TARGET_MM,
        config.MAX_VERTICAL_REVERSE_ANGLE
    )

    motion_control.stop_robot()

    if not success:
        print("Vertical parking failed during reverse")
        return False

    return True
    # return final_safety_check()


def reverse_curve_for_motor_angle(max_motor_angle, speed=config.PARKING_SPEED):
    motion_control.reset_drive_motors()

    while motion_control.average_motor_angle() < max_motor_angle:
        if stop_if_too_close():
            return True

        # reverse curve into the parking spot
        left_speed = -speed + config.MAX_PARKING_CORRECTION
        right_speed = -speed - config.MAX_PARKING_CORRECTION

        motion_control.drive(left_speed, right_speed)

        print(
            "curve motor:", motion_control.average_motor_angle(),
            "rear:", read_filtered_rear_distance(),
            "side:", read_filtered_side_distance()
        )

        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()
    return True


def reverse_straight_for_motor_angle(target_angle, speed=config.PARKING_SPEED):
    motion_control.reset_drive_motors()
    motion_control.reset_gyro()

    while motion_control.average_motor_angle() < target_angle:
        if stop_if_too_close():
            return True

        motion_control.reverse_straight_with_gyro(speed)

        print(
            "backup motor:", motion_control.average_motor_angle(),
            "rear:", read_filtered_rear_distance()
        )

        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()
    return True


def perform_parallel_parking(gap_length):
    hardware.ev3.speaker.beep()
    print("Performing parallel parking")

    # Step 1: back up straight to better entry position
    success = reverse_straight_for_motor_angle(
        config.PARALLEL_BACKUP_BEFORE_TURN_ANGLE
    )

    if not success:
        print("Parallel parking failed during straight backup")
        return False

    wait(200)

    # Step 2: angle toward the parking spot
    motion_control.turn_in_place_with_gyro(config.PARALLEL_FIRST_TURN_ANGLE)

    wait(300)

    # Step 3: back up more after turning, before curving
    print("Step 3: angled straight backup")
    success = reverse_straight_for_motor_angle(
        config.PARALLEL_BACKUP_BEFORE_REVERSE_ANGLE
    )

    if not success:
        print("Parallel parking failed during angled straight backup")
        return False

    wait(200)


    # Step 4: reverse curve into the spot
    success = reverse_curve_for_motor_angle(
        config.MAX_PARALLEL_FIRST_REVERSE_ANGLE
    )

    motion_control.stop_robot()

    if not success:
        print("Parallel parking failed during reverse curve")
        return False

    # return final_safety_check()
    return True