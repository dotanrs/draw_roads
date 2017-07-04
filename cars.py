import perspective as pr


class car:
    def __init__(self, distance, lane):
        self.distance = distance
        self.lane = lane

    def draw(self, road, draw):
        car_image_start, car_image_start_y = road.lane_position(self.distance, self.lane, pr.CAR_WIDTH)

        car_image_width = pr.observed_width(self.distance, pr.CAR_WIDTH)
        car_image_height = pr.observed_width(self.distance, pr.CAR_HEIGHT)

        draw.rectangle(
            [car_image_start,
             pr.IMAGE_HEIGHT - car_image_start_y,
             car_image_start + car_image_width,
             pr.IMAGE_HEIGHT - car_image_start_y - car_image_height],
            fill="red")
