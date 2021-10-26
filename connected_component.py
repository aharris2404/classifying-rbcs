from PIL.Image import open as image_open
from PIL.ImageOps import grayscale
import numpy as np
import PIL.Image.Image

# dave = Image("./some_path.png")
# dave.image.show()
# dave.data

class Image():
    def __init__(self, path):
        self.image = image_open(path)
        self.data = np.array(self.image)

    def grayscale(self):
        self.grayscale = grayscale(self.image)
        self.grayscale_data = np.array(self.grayscale)


class ConnectedComponent(Image):
    def __init__(self, seed_pixel, label):
        self.seed_pixel = seed_pixel
        self.pixels = {seed_pixel}
        self.label = label
        self.bound_box = {}

    def _add_pixel(self, pixel):
        self.pixels.add(pixel)

    def update_bound_box(self):
        pixels = self.pixels.copy()
        while pixels:
            comparee = pixels.pop()
            self.bound_box['x_min'] = min(self.bound_box.get('x_min', comparee.x), comparee.x)
            self.bound_box['x_max'] = max(self.bound_box.get('x_max', comparee.x), comparee.x)
            self.bound_box['y_min'] = min(self.bound_box.get('y_min', comparee.y), comparee.y)
            self.bound_box['y_max'] = max(self.bound_box.get('y_max', comparee.y), comparee.y)

    def gobble(self): #add new pixels that are nearby from a seed
        queue = self.pixels.copy()

        while queue():
            curr_pixel = queue.pop()
            neighbors = curr_pixel.get_cardinal_neighbors()

            for neighbor in neighbors:
                if neighbor.color == curr_pixel.color and neighbor not in self.pixels:
                    self.pixels.add(neighbor)
                    queue.add(neighbor)

class Pixel():
    X=None #the size of the x dimension of the image
    Y=None #the size of the y dimension of the image

    def __init__(self, x, y, color=None, X=None, Y=None):
        self.x = x
        self.y = y
        self.color = color
        if X:
            Pixel.X = X
        if Y:
            Pixel.Y = Y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_cardinal_neighbors(self):
        result = [(self.x+1, self.y),
                  (self.x-1, self.y),
                  (self.x, self.y+1),
                  (self.x, self.y-1)]
        neighbors = [Pixel(coordinate[0], coordinate[1]) for coordinate in result]
        return [(i, j) for (i, j) in result if (i >= 0) and i < Pixel.X and j >= 0 and j < Pixel.Y]