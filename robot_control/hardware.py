from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port


# Main EV3 brick
ev3 = EV3Brick()

# Sensors
color_sensor = ColorSensor(Port.S2)
side_ultrasonic = UltrasonicSensor(Port.S3)
rear_ultrasonic = UltrasonicSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S1)

# Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)