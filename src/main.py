from pathlib import Path

import numpy as np

from image_handler.image_handler import ImageHandler
from image_handler.filters import Filters

def main():
    filters = Filters()
    im_folder = Path("images")

    p = im_folder.glob("**/*")
    images = [x for x in p if x.is_file()]

    for image in images:
        im_array = filters.run_initial_pipeline(image)
        im_graph = ImageHandler(im_array)



if __name__ == "__main__":

    main()