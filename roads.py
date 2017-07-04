import perspective as pr
import cv2
import numpy as np
from PIL import Image, ImageDraw


class AbstractRoad:
    def __init__(self, num_lanes):
        self.observed_height = pr.observed_height
        self.observed_width = pr.observed_width
        self.lane_width = pr.LANE_WIDTH
        self.num_lanes = num_lanes
        self.image_width = pr.IMAGE_WIDTH
        self.road_length = pr.ROAD_LENGTH
        self.image_height = pr.IMAGE_HEIGHT

    def lane_position(self, obj_distance, lane_num, obj_width=0.0):
        pass

    def draw(self, drawer):
        pass


class StraightRoad(AbstractRoad):
    def __init__(self, num_lanes):
        super().__init__(num_lanes)

    def lane_position(self, obj_distance, lane_num, obj_width=0.0):
        lane_y_start_at_distance = self.observed_height(obj_distance)
        lane_width_at_distance = self.observed_width(obj_distance, self.lane_width)
        road_margin = (self.image_width - self.num_lanes * lane_width_at_distance) / 2
        obj_width_at_distance = self.observed_width(obj_distance, obj_width)
        lane_margin_left = (lane_num + 0.5) * lane_width_at_distance + road_margin - obj_width_at_distance / 2

        print(lane_num, obj_distance, lane_width_at_distance, road_margin, road_margin)

        return lane_margin_left, lane_y_start_at_distance

    def draw(self, drawer):
        road_visible_height = pr.observed_height(self.road_length)
        closest_visible_road_distance = pr.closest_visible_ground_distance()

        lane_width_on_screen_bottom = pr.observed_width(closest_visible_road_distance, self.lane_width)
        margin = (self.image_width - lane_width_on_screen_bottom * self.num_lanes) / 2

        lane_lines = [(margin + (i * lane_width_on_screen_bottom)) for i in range(self.num_lanes + 1)]
        lane_width_end = pr.observed_width(self.road_length, self.lane_width)

        margin_end = (self.image_width - lane_width_end * self.num_lanes) / 2
        lane_ends = [(margin_end + (i * lane_width_end)) for i in range(self.num_lanes + 1)]

        print(lane_width_on_screen_bottom, lane_width_end)

        # Draw lanes
        for lane in range(self.num_lanes + 1):
            lane_begin = lane_lines[lane]
            lane_end = lane_ends[lane]
            drawer.line((lane_begin, self.image_height, lane_end, self.image_height - road_visible_height))

