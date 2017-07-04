from PIL import Image, ImageDraw
import math
import roads
import perspective as pr
import cars as crs


def log_var(**kwargs):
    for k in kwargs:
        print("[VAR]", k, kwargs.get(k))


def draw_lanes(cars):
    num_lanes = 3

    im = Image.new('RGBA', (pr.IMAGE_WIDTH, pr.IMAGE_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    road = roads.StraightRoad(num_lanes)

    road.draw(draw)

    # Draw cars
    for car in cars:
        crs.car(car[1], car[0]).draw(road, draw)

    im.show()


if __name__ == "__main__":
    # List(List(car_lane, car_distance))
    default_cars = [
        [2, 10],
        [0, 5],
        [1, 1.3],
        [1, 20]
    ]
    draw_lanes(default_cars)
