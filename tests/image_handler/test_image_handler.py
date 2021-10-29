import unittest
import pathlib

from PIL import Image, ImageOps
import numpy as np

from src.image_handler.image_handler import ImageHandler

curr_path = pathlib.Path(__file__).parent.resolve()

class TestImageHandler(unittest.TestCase):


    def setUp(self):
        two_test_path = curr_path.joinpath("two_test.png")
        im = Image.open(two_test_path)
        im_gray = ImageOps.grayscale(im)
        im_array = np.array(im)
        gray_array = np.array(im_gray)
        self.image = ImageHandler(gray_array)
        

    def test_color_at(self):
        self.assertEqual(self.image.color_at((0, 0)), 0, "Top left pixel of two_test.png is black")
        self.assertEqual(self.image.color_at((3, 3)), 255, "Central pixel of two_test.png is white")

    def test_grow_component(self):
        component = self.image._grow_component((1,1), set([(i, j) for i in range(self.image.X) 
                                                                  for j in range(self.image.Y)]))
        
        self.assertEqual(len(component), 16, "Outer white ring should contain no white pixels")
        self.assertNotIn((0,0), component, "Outer black ring should not be in component")
        self.assertNotIn((2,2), component, "Inner black ring should not be in component")
        self.assertNotIn((3,3), component, "Inner white ring should not be in component")

    def test_find_connected_components(self):
        components = self.image._find_connected_components(color=255)
        
        self.assertEqual(len(components), 2, "Two white components in two_test.png")
        self.assertListEqual(sorted([len(c.pixels) for c in components]), [1, 16], "Sorted lengths of two white components in two_test.png")

    def test_filter_contained_boxes(self):
        self.image.filter_contained_boxes()

        self.assertEqual(len(self.image.connected_components), 1, "Only one component after filteration in two_test.png")
        
        # TODO: write function in image handler to access each component in connected_components
        # self.assertEqual(self.image.connected_components, 17, "Components should be added together")
        # self.assertEqual(self.image.connected_components.label, 0, "Label should update to smallest label in addition")


    def test_color_image_failure(self):
        pass


if __name__ == "__main__":
    unittest.main()
