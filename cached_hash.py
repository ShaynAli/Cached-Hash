"""
Caches the hash of a subclass.
This allows for the efficient use of dicts in cases when subclasses are rarely mutated.
"""
from abc import ABCMeta

# Alternative ideas:
#   * Have a list of safe_names
#   * Have 'hash_determiners', which are a list of variables which are used to determine the hash and are monitored for
#     changes to invalidate the hash

# TODO: Surveil self.<variable> changes to hash_determiners and implement


class CachedHash:

    hash_mutators = {}

    @staticmethod
    def set_mutators(mutator_set):
        CachedHash.hash_mutators = mutator_set

    def __init__(self, verbose=False):
        self.__hash = None
        self._verbose = verbose

    def __hash__(self):
        if self.__hash is None:
            self.__hash = object.__hash__(self)
            self._vprint(f'Set hash to {self.__hash}')
        return self.__hash

    def __getattribute__(self, item):
        if item in CachedHash.hash_mutators:
            self.__invalidate_hash()
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key in CachedHash.hash_mutators:
            self.__invalidate_hash()
        return super().__setattr__(key, value)

    def __invalidate_hash(self):
        self.__hash = None
        self._vprint('Invalidated hash')

    def _vprint(self, msg, *args, **kwargs):
        if self._verbose:
            print(msg, *args, **kwargs)


class Example(CachedHash):

    def __init__(self, a=None, b=10, c='default'):
        super().__init__(verbose=True)
        super().set_mutators({
            'reset'
        })
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return f'Example(a: {self.a}, b: {self.b}, c: {self.c})'

    def reset(self):
        self.a = None
        self.b = 10
        self.c = 'default'

    def safe_method(self):
        print('I am safe to call, as I do not invalidate the hash')


if __name__ == '__main__':
    print(f'Here is an example object which inherits from {CachedHash.__name__}, play around with it!')
    example = Example()
    breakpoint()
