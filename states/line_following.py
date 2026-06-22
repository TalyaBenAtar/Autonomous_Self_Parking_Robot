# from pybricks.tools import wait

# import robot_control.hardware as hardware
# import robot_control.motion_control as motion_control
# import config

# # Test the color sensor readings
# def test_color_sensor():
#     while True:
#         print(hardware.color_sensor.reflection())
#         wait(200)

# def read_line_reflection():
#     """
#     Reads the reflected light value from the color sensor.

#     Reflection values are usually:
#     - lower on dark/black areas
#     - higher on light/white areas
#     """

#     return hardware.color_sensor.reflection()


# def calculate_line_error(reflection):
#     """
#     Calculates how far the current reflection is from the target reflection.
#     """

#     return config.LINE_TARGET_REFLECTION - reflection


# def limit_correction(correction):
#     """
#     Limits the correction value so the robot does not turn too aggressively.
#     """

#     if correction > config.MAX_LINE_CORRECTION:
#         return config.MAX_LINE_CORRECTION

#     if correction < -config.MAX_LINE_CORRECTION:
#         return -config.MAX_LINE_CORRECTION

#     return correction


# def calculate_line_correction(reflection):
#     """
#     Calculates the motor correction according to the color sensor reading.
#     """

#     error = calculate_line_error(reflection)
#     correction = error * config.LINE_KP

#     return limit_correction(correction)


# def follow_line():
#     """
#     Performs one line-following step.

#     This function should be called repeatedly by main or by another state controller.
#     It does not contain its own loop, so it does not take control away from the state machine.
#     """

#     reflection = read_line_reflection()
#     correction = calculate_line_correction(reflection)

#     left_speed = config.DRIVE_SPEED + correction
#     right_speed = config.DRIVE_SPEED - correction

#     print("ref:", reflection, "corr:", correction, "L:", left_speed, "R:", right_speed)

#     motion_control.drive(left_speed, right_speed)


# def prepare_line_following():
#     """
#     Prepares the robot before starting a line-following state.
#     """

#     motion_control.reset_gyro()
#     motion_control.reset_drive_motors()


# def stop_line_following():
#     """
#     Stops the robot after line following.
#     """

#     motion_control.stop_robot()


# def print_line_reflection_for_testing():
#     """
#     Prints color sensor reflection values.
#     Use this to calibrate LINE_TARGET_REFLECTION.
#     """

#     while True:
#         print(read_line_reflection())
#         wait(200)


# def follow_line_for_testing():
#     """
#     Temporary test function for calibrating line following.
#     Runs forever until the program is stopped manually.
#     """

#     prepare_line_following()

#     while True:
#         follow_line()
#         wait(config.MAIN_LOOP_WAIT_MS)