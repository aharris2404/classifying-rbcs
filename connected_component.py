import numpy as np

class ImageHandler():
    def __init__(self, array): #array might be 2d or 3d
        try:
            if len(shape.array) > 2:
                raise NotImplementedError
            
            self.array = array
            self.X, self.Y = array.shape[0], array.shape[1]
            self.connected_components = self._find_connected_components()
        except Exception as inst: 
            print("Only grayscale images supported currently")


    def _grow_component(self, seed, unvisited):

        queue = [seed]
        component = {seed}

        while queue:
            curr_pixel = queue.pop()
            all_neighbors = self._get_cardinal_neighbors(curr_pixel)
            unvisited_neighbors = [neighbor for neighbor in all_neighbors 
                                    if self.color_at(neighbor) == self.color_at(curr_pixel)
                                    and neighbor in unvisited]

            unvisited = unvisited - set(unvisited_neighbors)
            component.add(unvisited_neighbors)

            queue.extend(unvisited_neighbors)

        return component


    def _find_connected_components(self, color=255):
        xs, ys = np.where(self.array == color)
        unvisited_pixels = set(zip(xs, ys))
        result = {}
        label = 0

        while unvisited_pixels:
            seed_pixel = unvisited_pixels.pop()

            curr_component = self._grow_component(seed_pixel, unvisited_pixels)  
            result.add(ConnectedComponent(seed_pixel, curr_component, label))
            label += 1
        
        return result


    def color_at(self, loc):
        x, y = loc
        return self.array[x][y]

    def _get_cardinal_neighbors(self, loc):
        x, y = loc
        neighbors = [(x - 1, y), (x + 1, y), (x, y-1), (x, y+1)]
        return [(i, j) for i, j in neighbors if 0 <= i and i < self.X and 0 <= j and j < self.Y]


    def _filter_contained_boxes(self):
        # compare boxes around connected components and merge any box contained in another box
        return None

class ConnectedComponent():
    def __init__(self, seed_pixel, component, label): #refactor to move growing components into image handler
        self.seed_pixel = seed_pixel
        self.pixels = component
        self.label = label
        self.bound_box = {}

    def _add_pixel(self, pixel):
        self.pixels.add(pixel)

    def update_bound_box(self):
        pixels = self.pixels.copy()
        while pixels:
            x, y = pixels.pop()
            self.bound_box['x_min'] = min(self.bound_box.get('x_min', x), x)
            self.bound_box['x_max'] = max(self.bound_box.get('x_max', x), x)
            self.bound_box['y_min'] = min(self.bound_box.get('y_min', y), y)
            self.bound_box['y_max'] = max(self.bound_box.get('y_max', y), y)
    
    def __hash__(self):
        return hash(self.label)
        
    def __add__(self, new_component):
        return None

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
