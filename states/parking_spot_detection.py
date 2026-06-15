from pybricks.tools import wait

import config
import robot_control.hardware as hardware
import robot_control.motion_control as motion_control


class ParkingType:
    UNKNOWN = 0
    TOO_SMALL = 1
    VERTICAL = 2
    PARALLEL = 3


def read_side_distance():
    return hardware.side_ultrasonic.distance()


def read_filtered_side_distance():
    total = 0

    for _ in range(config.ULTRASONIC_FILTER_SAMPLES):
        total += read_side_distance()
        wait(config.ULTRASONIC_FILTER_WAIT_MS)

    return total / config.ULTRASONIC_FILTER_SAMPLES


def is_gap(distance_mm):
    return distance_mm >= config.SIDE_DISTANCE_GAP_THRESHOLD_MM


def classify_gap(gap_length_mm):
    if gap_length_mm >= config.MIN_PARALLEL_GAP_MM:
        return ParkingType.PARALLEL

    if gap_length_mm >= config.MIN_VERTICAL_GAP_MM:
        return ParkingType.VERTICAL

    return ParkingType.TOO_SMALL


def prepare_parking_spot_detection():
    motion_control.reset_drive_motors()
    motion_control.reset_gyro()


# def detect_and_classify_parking_spot():
#     """
#     State 1 already detected the beginning of the gap.
#     This state continues driving forward, measures the gap length,
#     and classifies it as VERTICAL, PARALLEL, or TOO_SMALL.
#     """

#     prepare_parking_spot_detection()

#     gap_start_angle = 0

#     while motion_control.average_motor_angle() < config.MAX_GAP_SEARCH_MOTOR_ANGLE :
#         distance = read_filtered_side_distance()

#         print("side distance:", distance)

#         motion_control.drive_straight_with_gyro(config.GAP_DETECTION_SPEED)

#         if not is_gap(distance):
#             gap_end_angle = motion_control.average_motor_angle()
#             gap_length = gap_end_angle - gap_start_angle

#             motion_control.stop_robot()

#             parking_type = classify_gap(gap_length)

#             print("Gap ended")
#             print("Gap length:", gap_length)
#             print("Parking type:", parking_type)

#             return parking_type, gap_length

#         wait(config.MAIN_LOOP_WAIT_MS)

#     motion_control.stop_robot()
#     return ParkingType.UNKNOWN, 0


def detect_and_classify_parking_spot():
    prepare_parking_spot_detection()

    print("Searching for gap start")

    # Step 1: drive until side sensor sees empty space
    while motion_control.average_motor_angle() < config.MAX_GAP_SEARCH_DISTANCE_MM:
        distance = read_filtered_side_distance()
        print("search side distance:", distance)

        motion_control.drive_straight_with_gyro(config.GAP_DETECTION_SPEED)

        if is_gap(distance):
            print("Gap started")
            motion_control.stop_robot()
            break

        wait(config.MAIN_LOOP_WAIT_MS)

    else:
        motion_control.stop_robot()
        return ParkingType.UNKNOWN, 0

    # Step 2: measure the gap length
    motion_control.reset_drive_motors()

    print("Measuring gap")

    while motion_control.average_motor_angle() < config.MAX_GAP_SEARCH_DISTANCE_MM:
        distance = read_filtered_side_distance()
        print("gap side distance:", distance)

        motion_control.drive_straight_with_gyro(config.GAP_DETECTION_SPEED)

        if not is_gap(distance):
            gap_length = motion_control.average_motor_angle()
            motion_control.stop_robot()

            parking_type = classify_gap(gap_length)

            print("Gap ended")
            print("Gap length:", gap_length)
            print("Parking type:", parking_type)

            return parking_type, gap_length

        wait(config.MAIN_LOOP_WAIT_MS)

    motion_control.stop_robot()
    return ParkingType.UNKNOWN, 0