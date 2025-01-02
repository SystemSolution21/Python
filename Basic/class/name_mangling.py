# Name mangling letting subclass to override methods
# without breaking intraclass method calls.


class Mapping:

    def __init__(self, iterable) -> None:
        self.item_list = []
        self.__update(iterable=iterable)

    def update(self, iterable) -> None:
        for item in iterable:
            self.item_list.append(item)

    __update = update  # private copy of original update() method


class MappingSubclass(Mapping):

    def update(self, keys, values) -> None:
        """provides new signature for update()
        but does not break __init__()

        Args:
            keys (_type_): iterable
            values (_type_): iterable
        """
        for item in zip(keys, values):
            self.item_list.append(item)
