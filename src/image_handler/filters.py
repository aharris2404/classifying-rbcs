import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import difference_of_gaussians, sobel, \
                            threshold_local, threshold_li
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage.filters.thresholding import try_all_threshold


class Filters():

    def __init__(self):
        pass
    
    @staticmethod
    def show_image(image):
        plt.imshow(image, interpolation='nearest', cmap="gray")
        plt.show()

    def open_image(self, path):
        return io.imread(path)
    
    # high pass filter by subtracting a low pass filter
    def high_pass(self, image):
        low_pass = ndimage.gaussian_filter(image, 4.0)
        return image - low_pass

    def invert_grayscale(self, image):
        invert_func = lambda x: 255 - x
        vect_inverse = np.vectorize(invert_func)

        return vect_inverse(image)

    def run_initial_pipeline(self, im_path):
        # open image
        im = self.open_image(im_path)

        # TODO: Investigate upsampling the image

        # Step 1: Edge enhancement
        high_pass_im = self.high_pass(im)
        enhanced_im = difference_of_gaussians(high_pass_im, 0.5)

        # Step 2: Sobel Edge Detection
        edges = sobel(enhanced_im)

        # Step 3: Grayscale
        grayscaled = rgb2gray(edges)

        # Step 3: Threshholding

        # Adaptive Thresholding Method:
        block_size = 35
     
        thresh_array = threshold_local(image=rgb2gray(im), block_size=block_size)

        # # Note: try_all_threshold in skimage.filters will show outputs from various thresholding methodologies
        thresh = threshold_li(grayscaled)
        binary = grayscaled > thresh
        global_thresh_array = np.zeros(shape=binary.shape)
        global_thresh_array[binary] += 255

        
        # TODO: Investigate fancier thresholding techniques and sweeping over the image
        
        return self.invert_grayscale(global_thresh_array)


if __name__ == "__main__":
    im_path = "./1.tif"
    filters = Filters()

    image = filters.run_initial_pipeline(im_path)
    print(image.shape)
    filters.show_image(image)

# TODO: Investigate image scaling for ETL purposes when extracting cells

