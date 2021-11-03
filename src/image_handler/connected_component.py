class ConnectedComponent():
    def __init__(self, seed_pixel, component, label): #refactor to move growing components into image handler
        self.seed_pixels = [seed_pixel]
        self.pixels = component
        #TODO: Verify seed_pixel in pixels
        self.label = label
        self.bound_box = {}
        self._update_bound_box()
        self.size_changed = False

    def clear(self):
        self.seed_pixels = []
        self.pixels = set()
        self.label = None
        self.bound_box = {}


    def _update_bound_box(self):
        pixels = self.pixels.copy()
        while pixels:
            x, y = pixels.pop()
            self.bound_box['x_min'] = min(self.bound_box.get('x_min', x), x)
            self.bound_box['x_max'] = max(self.bound_box.get('x_max', x), x)
            self.bound_box['y_min'] = min(self.bound_box.get('y_min', y), y)
            self.bound_box['y_max'] = max(self.bound_box.get('y_max', y), y)
    
    def get_bound_box(self):
        if self.size_changed:
            self._update_bound_box()

        return (self.bound_box['x_min'], self.bound_box['y_min'],
                self.bound_box['x_max'], self.bound_box['y_max'])

    def _get_bound_keys(self):
        return ("x_min", "y_min", "x_max", "y_max")

    def contains(self, other):
        x_min, y_min, x_max, y_max = self.get_bound_box()
        i_min, j_min, i_max, j_max = other.get_bound_box()
        return x_min <= i_min and y_min <= j_min and x_max >= i_max and y_max >= j_max
    
    def __hash__(self):
        return hash(self.label)

    def __add__(self, other):
        self.seed_pixels.extend(other.seed_pixels)
        self.pixels |= other.pixels
        self.label = min(self.label, other.label)

        #update bounding boxes
        # TODO: Test this formulation
        zipped_bounds = zip(self.get_bound_box(), other.get_bound_box())
        funcs = [lambda x, y: min(x, y), lambda x, y: min(x, y), 
                 lambda x, y: max(x, y), lambda x, y: max(x, y)]
        self.bound_box = {
            key: func(c, o) for key, (c, o), func in zip(self._get_bound_keys(), zipped_bounds, funcs)
        }

        return self



    
    def __eq__(self, other):
        return self.label == other.label

    # Returns true if component contains pixels
    def __bool__(self):
        return bool(self.pixels)

    def __len__(self):
        return len(self.pixels)
