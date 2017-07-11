from PIL import Image, ImageDraw
import perspective as pr
import numpy as np
import matplotlib.pyplot as plt


class AbstractImage:
    def __init__(self):
        self.image_width = pr.IMAGE_WIDTH
        self.image_height = pr.IMAGE_HEIGHT

    def line(self, x1, y1, x2, y2):
        pass

    def bitmap(self, start_pos, data):
        pass

    def show(self):
        pass

    def rectangle(self, coords, fill):
        pass

    def get(self):
        pass


class PilImage(AbstractImage):
    def __init__(self):
        super().__init__()
        self.im = Image.new('RGBA', (self.image_width, self.image_height), (0, 0, 0, 0))
        self.drawer = ImageDraw.Draw(self.im)

    def bitmap(self, start_pos, data):
        a = Image.new("L", (self.image_width, self.image_height), 0)
        a.putdata(data.reshape([self.image_height * self.image_width]))
        self.drawer.bitmap(start_pos, a)

    def line(self, x1, y1, x2, y2):
        self.drawer.line((x1, y1, x2, y2))

    def show(self):
        self.im.show()

    def rectangle(self, coords, fill):
        self.drawer.rectangle(
            coords,
            fill=fill)


class NpArray(AbstractImage):
    def __init__(self):
        super().__init__()
        self.arr = np.zeros((self.image_width, self.image_height, 3))

    def bitmap(self, start_pos, data):
        dx = len(data)
        dy = len(data[0])
        for a in range(dx):
            for b in range(dy):
                x = start_pos[0] + a
                y = start_pos[1] + b
                if 0 <= x < pr.IMAGE_WIDTH and 0 <= y < self.image_height:
                    self.arr[int(x), int(y)] = data[a, b]

    def show(self):
        plt.imshow(self.arr)
        plt.show()

    def line(self, x1, y1, x2, y2):
        from skimage.draw import line_aa
        rr, cc, val = line_aa(int(y1), int(x1), int(y2), int(x2))

        nrr = []
        ncc = []
        for i in range(len(rr)):
            r = rr[i]
            c = cc[i]
            if 0 < c < self.image_height and 0 < r < self.image_width:
                nrr.append(r)
                ncc.append(c)

        self.arr[nrr,
                 ncc,
                 :] = 100

    def rectangle(self, coords, fill):
        start = [min(coords[1], coords[3]), min(coords[0], coords[2])]
        width = max(coords[1], coords[3]) - start[0]
        height = max(coords[0], coords[2]) - start[1]

        data = np.ones([width, height]) * 100
        self.bitmap(start, data)

    def get(self):
        return self.arr