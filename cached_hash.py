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

    safe_names = {
        # Class specific
        '__hash',
        # The rest are from https://docs.python.org/3/reference/datamodel.html
        # region User-defined functions
        '__doc__',
        '__name__',
        # endregion
        # region 3.3.1. Basic customization
        '__repr__',
        '__str__',
        '__bytes__',
        '__format__',
        '__lt__',
        '__le__',
        '__eq__',
        '__ne__',
        '__gt__',
        '__ge__',
        '__hash__',
        '__bool__',
        # endregion
        # region 3.3.2. Customizing attribute access
        '__getattr__',
        '__getattribute__',
        '__dir__',
        # endregion
        # region 3.3.7. Emulating container types
        '__len__',
        '__length_hint__',
        '__getitem__',
        '__iter__',
        '__reversed__',
        '__contains__',
        # endregion
        # region 3.3.8. Emulating numeric types
        '__add__',
        '__sub__',
        '__mul__',
        '__matmul__',
        '__truediv__',
        '__floordiv__',
        '__mod__',
        '__divmod__',
        '__pow__',
        '__lshift__',
        '__rshift__',
        '__and__',
        '__xor__',
        '__or__',
        '__radd__',
        '__rsub__',
        '__rmul__',
        '__rmatmul__',
        '__rtruediv__',
        '__rfloordiv__',
        '__rmod__',
        '__rdivmod__',
        '__rpow__',
        '__rlshift__',
        '__rrshift__',
        '__rand__',
        '__rxor__',
        '__ror__',
        '__neg__',
        '__pos__',
        '__abs__',
        '__invert__',
        '__complex__',
        '__int__',
        '__float__',
        '__index__',
        '__round__',
        '__trunc__',
        '__floor__',
        '__ceil__'
        # endregion
    }

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

    # safe_names = CachedHash.safe_names.union({
    #     'safe_method'
    # })

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
