import perspective as pr


class Car:
    def __init__(self, lane, distance, speed=0):
        self.distance = distance  # meters
        self.lane = lane  # 0 .. num_lanes - 1
        self.speed = speed  # meters per second

    def draw(self, road, draw):
        car_image_start, car_image_start_y = road.lane_position(self.distance, self.lane, pr.CAR_WIDTH)

        car_image_width = pr.observed_width(self.distance, pr.CAR_WIDTH)
        car_image_height = pr.observed_width(self.distance, pr.CAR_HEIGHT)

        draw.rectangle(
            [car_image_start,
             car_image_start_y,
             car_image_start + car_image_width,
             car_image_start_y - car_image_height],
            fill="red")

        self.distance += self.speed
