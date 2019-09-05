"""
Caches the hash of a subclass.
This allows for the efficient use of dicts in cases when subclasses are rarely mutated.
"""


class CachedHash(object):

    default_safe_names = frozenset({
        '__hash'
    })

    def _subclass(self):
        return self.__class__.mro()[0]

    def __getattribute__(self, item):  # TODO: Should be a set function/should we add checks to builtin set functions?
        breakpoint()  # TODO: Fix (WIP)
        if item == 'safe_names':
            return vars(self)['safe_names']
        if item not in self.safe_names:
            self.__hash = None
        return self._subclass().__getattribute__(item)

    def __init__(self, safe_names=default_safe_names):  # TODO: Identify good names to expect to be safe from mutations
        self.__hash = None
        self.safe_names = safe_names

    def __hash__(self):
        if self.__hash is not None:
            return self.__hash


class Example(CachedHash):

    def __init__(self, a=None, b=10):
        super().__init__()
        self.a = a
        self.b = b

    def reset(self):
        self.a = None
        self.b = 10
