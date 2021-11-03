from pathlib import Path
import logging

import numpy as np
from matplotlib import pyplot

from image_handler.image_handler import ImageHandler
from image_handler.filters import Filters

def main():
    #TODO: Add logging throughout app

    filters = Filters()
    im_folder = Path("images")

    # Find all files in images folder
    p = im_folder.glob("**/*")
    images = [x for x in p if x.is_file()]

    for image in images:
        im = filters.open_image(image)
        im_array = filters.run_initial_pipeline(image)

        # filters.show_image(im_array)
        
        # Find connected components in image
        im_graph = ImageHandler(im_array)

        im_graph.filter_components_by_size(min_size=100, max_size=3000)
        print(f"Post Size Filtering: We have {len(im_graph.connected_components.keys())} components")
        
        # im_graph.filter_contained_boxes()
        im_graph.filter_median_set_distance(tol=30)

        print(f"Post Closeness Filtering: We have {len(im_graph.get_components())}")


        # Display all the components algorithm above found
        bounding_box_mask = np.full(im_array.shape, False)
        for c in im_graph.get_components():
            min_x, min_y, max_x, max_y = c.get_bound_box()
            bounding_box_mask[min_x:max_x, min_y:max_y] = np.full((max_x - min_x, max_y - min_y), True)
        
        masked_im = im.copy()
        masked_im[bounding_box_mask, :] = 0

        pyplot.imshow(im)
        # pyplot.imshow(masked_im)
        pyplot.show()

        # filters.show_image(masked_im)


if __name__ == "__main__":

    main()