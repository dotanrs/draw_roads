import math
import roads
import perspective as pr
import cars as crs
import image
import copy
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip

frame_counter = 0


def log_var(**kwargs):
    for k in kwargs:
        print("[VAR]", k, kwargs.get(k))


def draw_lanes(cars, image_type=image.NpArray, road_args={"num_lanes": 3}, show=False):
    draw = image_type()
    road = roads.StraightRoad(**road_args)

    road.draw(draw)

    # Draw cars
    for car in cars:
        car.draw(road, draw)

    if show:
        draw.show()

    return draw.get()


def draw_movie(cars, num_frames, frames_per_second):
    frames = []

    cars = [crs.Car(distance=c.distance, lane=c.lane, speed=c.speed / frames_per_second) for c in cars]
    num_lanes = max([car.lane for car in cars]) + 1

    for i in range(num_frames):
        frames.append(draw_lanes(cars, image.NpArray, {"num_lanes": num_lanes}, show=False))

    def get_frame(t):
        global frame_counter
        frame = frames[frame_counter % len(frames)]
        frame_counter += 1
        return frame

    animation = VideoClip(get_frame, duration=math.floor(num_frames / frames_per_second))
    animation.write_videofile("cars1.mp4", fps=frames_per_second)


if __name__ == "__main__":

    cars = [
        crs.Car(1, 4, 1),
        crs.Car(2, 3, 0),
        crs.Car(0, 2, -1),
        crs.Car(2, 1.3, 3)
    ]

    draw_movie(cars, 200, 20)

    draw_lanes(cars, image.NpArray, {"num_lanes": 3}, show=True)

