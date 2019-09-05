"""
Caches the hash of a subclass.
This allows for the efficient use of dicts in cases when subclasses are rarely mutated.
"""


class CachedHash(object):

    def _subclass(self):
        return self.__class__.mro()[0]

    def __getattribute__(self, item):
        if item not in self.safe_names:
            self.__hash = None
        return self._subclass().__getattribute__(item)

    def __init__(self, safe_names=frozenset()):  # TODO: Identify good names to expect to be safe from mutations
        self.__hash = None
        self.safe_names = safe_names

    def __hash__(self):
        if self.__hash is not None:
            return self.__hash
