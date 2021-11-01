import numpy as np
from .connected_component import ConnectedComponent

class ImageHandler():
    def __init__(self, array, color=255): #array might be 2d or 3d
        try:
            if len(array.shape) != 2:
                raise NotImplementedError
            
            self.array = array
            self.X, self.Y = array.shape[0], array.shape[1]
            self.connected_components = self._find_connected_components(color=color)
        except NotImplementedError as inst: 
            print("Only grayscale images supported currently")


    def _grow_component(self, seed, unvisited):

        queue = [seed]
        component = {seed}

        while queue:
            curr_pixel = queue.pop(0)
            all_neighbors = self._get_cardinal_neighbors(curr_pixel)
            unvisited_neighbors = [neighbor for neighbor in all_neighbors 
                                    if self.color_at(neighbor) == self.color_at(curr_pixel)
                                    and neighbor in unvisited]

            unvisited -= set(unvisited_neighbors)
            component |= set(unvisited_neighbors)

            queue.extend(unvisited_neighbors)

        return component


    def _find_connected_components(self, color=255):
        xs, ys = np.where(self.array == color)
        unvisited_pixels = set(zip(xs, ys))
        result = set()
        label = 0

        while unvisited_pixels:
            seed_pixel = unvisited_pixels.pop()

            curr_component = self._grow_component(seed_pixel, unvisited_pixels)
            unvisited_pixels -= curr_component
            result.add(ConnectedComponent(seed_pixel, curr_component, label))

            label += 1
        
        return result


    def color_at(self, loc):
        x, y = loc
        return self.array[x][y]

    def get_components(self):
        return self.connected_components

    def _get_cardinal_neighbors(self, loc):
        x, y = loc
        neighbors = [(x - 1, y), (x + 1, y), (x, y-1), (x, y+1)]
        return [(i, j) for i, j in neighbors if 0 <= i and i < self.X and 0 <= j and j < self.Y]


    def filter_contained_boxes(self):
        # compare boxes around connected components and merge any box contained in another box
        # initial pass is O(n^2), can be improved to O(nlogn)

        component_pairs = set([(c, o) for c in self.connected_components
                                      for o in self.connected_components
                                      if c.label < o.label])

        for component, other in component_pairs:
            
            if component not in self.connected_components or other not in self.connected_components:
                continue

            if component.contains(other):
                component + other
                self.connected_components -= {other}
            
            elif other.contains(component):
                component + other
                self.connected_components -= {component}

    def get_component(self, label):
        for c in self.connected_components:
            if c.label == label:
                return c

        return False

    def filter_components_by_size(self, min_size=0, max_size=float('inf')):
        allowed_components = set()

        self.connected_components = set([c for c in self.connected_components 
                                            if len(c) >= min_size and len(c) <= max_size])


    def crop_to_component(self, label):
        component = self.get_component(label)

        if component:
            min_x, min_y, max_x, max_y = component.get_bound_box()
            return self.array[min_x:max_x, min_y:max_y]
