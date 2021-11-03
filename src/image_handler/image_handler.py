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
        result = {}
        label = 0

        while unvisited_pixels:
            seed_pixel = unvisited_pixels.pop()

            curr_component = self._grow_component(seed_pixel, unvisited_pixels)
            unvisited_pixels -= curr_component
            result[label] = ConnectedComponent(seed_pixel, curr_component, label)

            label += 1
        
        return result

    def _merge_components(self, component, other):
        merged = component + other
        self.connected_components.pop(component.label)
        self.connected_components.pop(other.label)

        self.connected_components[merged.label] = merged


    def color_at(self, loc):
        x, y = loc
        return self.array[x][y]

    def get_components(self):
        return self.connected_components.values()

    def get_component_pairs(self):
        return [(c, o) for c in self.connected_components.values()
                                      for o in self.connected_components.values()
                                      if c.label < o.label]


    def _get_cardinal_neighbors(self, loc):
        x, y = loc
        neighbors = [(x - 1, y), (x + 1, y), (x, y-1), (x, y+1)]
        return [(i, j) for i, j in neighbors if 0 <= i and i < self.X and 0 <= j and j < self.Y]

    def get_component(self, label):
        return self.connected_components.get(label, False) #TODO: change implemention to return iterator

    def crop_to_component(self, label):
        component = self.get_component(label)

        if component:
            min_x, min_y, max_x, max_y = component.get_bound_box()
            return self.array[min_x:max_x, min_y:max_y]

    ### Filters and distance metrics ###

    def filter_components_by_size(self, min_size=0, max_size=float('inf')):
        allowed_components = set()

        self.connected_components = {label:c for label, c in self.connected_components.items()
                                                        if len(c) >= min_size and len(c) <= max_size}
    
    def filter_contained_boxes(self):
        # compare boxes around connected components and merge any box contained in another box
        # initial pass is O(n^2), can be improved to O(nlogn)

        component_pairs = self.get_component_pairs()
        
        for component, other in component_pairs:
            c, o = component.label, other.label
            if c not in self.connected_components.keys() \
                or o not in self.connected_components.keys():
                continue

            if component.contains(other) or other.contains(component):
                self._merge_components(component, other)
        
                
    def filter_median_set_distance(self, tol=30):
        component_pairs = self.get_component_pairs()

        pairwise_distance = {}
        counter = 1

        for component, other in component_pairs:
            c, o = component.label, other.label
            if c not in self.connected_components.keys() \
                or o not in self.connected_components.keys():
                continue

            pairwise_distance[(c, o)] = self.median_set_distance(c, o)

            print(f"{counter}: Comparing components {c} and {o}")
            counter += 1
        
        print(len(pairwise_distance))
        for (c, o), distance in pairwise_distance.items():

            if distance <= tol:
                self._merge_components(self.get_component(c), self.get_component(o))
    
    
    def hausdorff_distance(self, other):
        pass

    
    def get_box_area(self, dims):
        x_min, y_min, x_max, y_max = dims
        return (x_max - x_min) * (y_max - y_min)


    def overlap_area(self, component, other):
        
        labels = ("x_min", "y_min", "x_max", "y_max")
        c_box, o_box = component.get_bound_box(), other.get_bound_box()
        funcs = (lambda x, y: max(x, y), lambda x, y: max(x, y),
                 lambda x, y: min(x, y), lambda x, y: min(x, y))

        overlap_box = {label:func(c, o) for label, c, o, func in zip(labels, c_box, o_box, funcs)}

        # Check for overlap by checking conditions on overlap_box
        if overlap_box["x_min"] >= overlap_box["x_max"] or overlap_box["y_min"] >= overlap_box["y_max"]:
            return 0
        
        # TODO: Replace with helper function
        return self.get_box_area(overlap_box("x_min"), overlap_box("y_min"),
                                 overlap_box("x_max")), overlap_box("y_max")


    def max_overlap_percent(self, component, other):
        area = self.overlap_area(component, other)
        c_area = self.get_box_area(component.get_bound_box())
        o_area = self.get_box_area(other.get_bound_box())

        return max(area)


    def median_set_distance(self, label1, label2):
        c, d = self.get_component(label1), self.get_component(label2)
        distances = []
        
        if c and d:
            distances = [abs(i - k) + abs(j - l) for i, j in c.pixels for k, l in d.pixels]

        return np.median(distances)

