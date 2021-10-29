import unittest
from src.image_handler.connected_component import ConnectedComponent

class TestConnectedComponent(unittest.TestCase):
    
    def setUp(self):
        self.seed = (0, 0)
        self.component = {(0,0), (0,1), (1, 1), (1, 2)}
        self.label = 0
        self.component = ConnectedComponent(self.seed, self.component, self.label)

    def tearDown(self):
        self.component.clear()

    
    def test_hash(self):
        self.assertEqual(hash(self.component), hash(self.label), "Hash should be based on a label")

    def test_clear(self):
        self.component.clear()
        self.assertIsNone(self.component.label, "Delete label on clear")
        self.assertListEqual(self.component.seed_pixels, [], "Clear list of seeds")
        self.assertSetEqual(self.component.pixels, set(), "Clear set of pixels in component")
        self.assertDictEqual(self.component.bound_box, {}, "Clear bounding box")

    def test_bounding_box(self):
        self.assertTupleEqual(self.component.get_bound_box(), (0, 0, 1, 2))

    def test_contains_on_strict_subset(self):
        other = ConnectedComponent((1, 1), set([(1, 1)]), 1)
        self.assertTrue(self.component.contains(other), "Strict subset ")
        self.assertFalse(other.contains(self.component))

    def test_contains_on_same_size_box(self):
        other = ConnectedComponent((0, 2), set([(0, 2), (1, 2), (0, 0)]), 1)
        self.assertTrue(self.component.contains(other), "Strict subset ")
        self.assertTrue(other.contains(self.component))

    def test_equals(self):
        pass

    def test_add(self):
        pass


if __name__ == "__main__":
    unittest.main()