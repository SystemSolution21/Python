import unittest
from name_mangling import Mapping, MappingSubclass


class TestMapping(unittest.TestCase):

    def test_init(self):
        m = Mapping([1, 2, 3])
        self.assertEqual(m.item_list, [1, 2, 3])

    def test_update(self):
        m = Mapping([])
        m.update([4, 5, 6])
        self.assertEqual(m.item_list, [4, 5, 6])


class TestMappingSubclass(unittest.TestCase):

    def test_init(self):
        ms = MappingSubclass([1, 2, 3])
        self.assertEqual(ms.item_list, [1, 2, 3])

    def test_update(self):
        ms = MappingSubclass([])
        ms.update([1, 2, 3], ["a", "b", "c"])
        self.assertEqual(ms.item_list, [(1, "a"), (2, "b"), (3, "c")])


if __name__ == "__main__":
    unittest.main()
