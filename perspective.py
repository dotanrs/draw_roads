import math

ELEVATION = 1
METER_PIXEL_RATIO = 500
EYE_ANGLE_Y = 65
HALF_EYE_ANGLE = 60
LOOK_DOWN_ANGLE = 10

# sizes (in meters)
CAR_WIDTH = 1.85
CAR_HEIGHT = 1.7
ROAD_LENGTH = 300
LANE_WIDTH = 2.5

# other settings
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400


def observed_height(distance):
    angel_to_edge = math.degrees(math.atan(float(ELEVATION) / distance)) - LOOK_DOWN_ANGLE
    return METER_PIXEL_RATIO * (EYE_ANGLE_Y / 2 - angel_to_edge) / EYE_ANGLE_Y


def observed_width(object_distance, absolute_width, half_angle=HALF_EYE_ANGLE):
    actual_distance = math.sqrt(object_distance ** 2 + ELEVATION ** 2)
    width_visible = actual_distance / math.tan(half_angle) * 2
    return (float(absolute_width) / width_visible) * METER_PIXEL_RATIO


def closest_visible_ground_distance():
    lowest_view_angle = 90 - EYE_ANGLE_Y - LOOK_DOWN_ANGLE
    return math.tan(lowest_view_angle) * ELEVATION
