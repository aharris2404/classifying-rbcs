import unittest
import pathlib

from PIL import Image, ImageOps
import numpy as np

from src.image_handler.image_handler import ImageHandler

curr_path = pathlib.Path(__file__).parent.resolve()

class TestImageHandler(unittest.TestCase):

    def setUp(self):
        self.two_test_path = curr_path.joinpath("two_test.png")
        self.checker_test_path = curr_path.joinpath("checker_test.png")
        
        
    def tearDown(self):
        self.image = None

    def path_to_images(self, path):
        im = Image.open(path)
        im_gray = ImageOps.grayscale(im)
        im_array = np.array(im)
        gray_array = np.array(im_gray)
        self.image = ImageHandler(gray_array)

    def test_color_image_failure(self):
        pass

    def test_two_component_image(self):
        self.path_to_images(self.two_test_path)

        # test color_at function
        self.assertEqual(self.image.color_at((0, 0)), 0, "Top left pixel of two_test.png is black")
        self.assertEqual(self.image.color_at((3, 3)), 255, "Central pixel of two_test.png is white")

        # test initially grown components
        component = self.image._grow_component((1,1), set([(i, j) for i in range(self.image.X) 
                                                                  for j in range(self.image.Y)]))

        self.assertEqual(len(component), 16, "Outer white ring should contain no white pixels")
        self.assertNotIn((0,0), component, "Outer black ring should not be in component")
        self.assertNotIn((2,2), component, "Inner black ring should not be in component")
        self.assertNotIn((3,3), component, "Inner white ring should not be in component")
        
        components = self.image._find_connected_components(color=255)
        self.assertEqual(len(components), 2, "Two white components in two_test.png")
        self.assertListEqual(sorted([len(c.pixels) for c in components]), [1, 16], "Sorted lengths of two white components in two_test.png")
        
        # test filtering of boxes contained in other boxes
        self.image.filter_contained_boxes()

        self.assertEqual(len(self.image.connected_components), 1, "Only one component after filteration in two_test.png")
        
        new_component = self.image.get_component(0)
        self.assertEqual(len(new_component.pixels), 17, "Components should be added together")
        self.assertFalse(self.image.get_component(1), "Component 1 should not exist")
    
    def test_checkered_image(self):
        self.path_to_images(self.checker_test_path)

        component_number = len(self.image.connected_components)

        self.assertEqual(component_number, 24, "There are 24 white pixels in checker_test.png")

        self.image.filter_contained_boxes()
        new_number = len(self.image.connected_components)

        self.assertEqual(component_number, new_number, "All singleton pixels are not contained in any other component")


if __name__ == "__main__":
    unittest.main()
