import unittest
from name_mangling import Mapping, MappingSubclass


class TestMapping(unittest.TestCase):

    def test_init(self) -> None:
        m = Mapping(iterable=[1, 2, 3])
        self.assertEqual(first=m.item_list, second=[1, 2, 3])

    def test_update(self) -> None:
        m = Mapping(iterable=[])
        m.update(iterable=[4, 5, 6])
        self.assertEqual(first=m.item_list, second=[4, 5, 6])


class TestMappingSubclass(unittest.TestCase):

    def test_init(self) -> None:
        ms = MappingSubclass(iterable=[1, 2, 3])
        self.assertEqual(first=ms.item_list, second=[1, 2, 3])

    def test_update(self) -> None:
        ms = MappingSubclass(iterable=[])
        ms.update(keys=[1, 2, 3], values=["a", "b", "c"])
        self.assertEqual(first=ms.item_list, second=[(1, "a"), (2, "b"), (3, "c")])


if __name__ == "__main__":
    unittest.main()
