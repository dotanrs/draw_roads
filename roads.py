import perspective as pr
import cv2
import numpy as np
from PIL import Image, ImageDraw
import math


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
        lane_y_start_at_distance = self.image_height - self.observed_height(obj_distance)
        lane_width_at_distance = self.observed_width(obj_distance, self.lane_width)
        road_margin = (self.image_width - self.num_lanes * lane_width_at_distance) / 2
        obj_width_at_distance = self.observed_width(obj_distance, obj_width)
        lane_margin_left = (lane_num + 0.5) * lane_width_at_distance + road_margin - obj_width_at_distance / 2

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

        # Draw lanes
        for lane in range(self.num_lanes + 1):
            lane_begin = lane_lines[lane]
            lane_end = lane_ends[lane]
            drawer.line(lane_begin, self.image_height, lane_end, self.image_height - road_visible_height)


class CurvedRoad(AbstractRoad):
    def __init__(self, num_lanes):
        super().__init__(num_lanes)
        self.offsets = []
        self.polly = [0.0018294279, 2.89854798e-01, 0]
        self.offsets = [50, 150, 250, 350]

        self.warp_matrix = cv2.getPerspectiveTransform(np.array([
            [0, 0],
            [self.image_width, 0],
            [self.image_width, self.image_height],
            [0, self.image_height]
        ], dtype=np.float32), np.array([
            # [0, 100],
            # [0, self.image_height],
            # [self.image_width, self.image_height],
            # [self.image_width, 0]
            [0.3125 * self.image_width, 0.6375 * self.image_height],
            [0.68671875 * self.image_width, 0.6375 * self.image_height],
            [1.76374092 * self.image_width, self.image_height],
            [-0.76373472 * self.image_width, self.image_height]
        ], dtype=np.float32))

        self.do_warp = True

    def warp(self, dots):
        return cv2.warpPerspective(dots, self.warp_matrix, (self.image_width, self.image_height))

    def draw(self, drawer):

        global_mask = np.zeros([self.image_width, self.image_height])

        for offset in self.offsets:

            polly = self.polly
            polly[2] = offset

            ploty = np.linspace(0, self.image_width - 1, self.image_height)
            fitx = polly[0] * ploty ** 2 + polly[1] * ploty + polly[2]
            n = np.array([fitx, ploty], dtype=np.int32).T

            mask = np.zeros([self.image_width, self.image_height])

            dots = [(a[1], a[0]) for a in n]

            for d in dots:
                if d[1] > 0 and (d[1] < self.image_height):
                    mask[self.image_height - 1 - d[0], d[1]] = 255

            global_mask += mask

        warped = self.warp(global_mask)

        ouptut = warped if self.do_warp else global_mask

        drawer.bitmap([0, 0], ouptut)

    def lane_position(self, obj_distance, lane_num, obj_width=0.0):

        dont_show_object = -100, -100
        distance_in_pixels = pr.observed_height(obj_distance)

        polly = self.polly
        polly[2] = self.offsets[lane_num]

        fitx = polly[0] * distance_in_pixels ** 2 + polly[1] * distance_in_pixels + polly[2]
        fity = self.image_height - distance_in_pixels
        if not self.do_warp:
            return fitx, fity

        mask = np.zeros([self.image_width, self.image_height])
        if fitx > self.image_width or fity > self.image_height:
            return dont_show_object

        mask[int(fitx), int(fity)] = 1

        aaaa = np.array([fitx, fity, 1], dtype=np.float32)
        warped = self.warp_matrix.dot(aaaa)
        warped /= warped[2]
        warped = warped[:2]

        return warped[0], warped[1]

