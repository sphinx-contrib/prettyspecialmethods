# Explicit empty docstrings prevent some kind of automatic or inherited
# docstring for certain methods.

class MethodHolder:
    # misc (alphabetical)
    def __await__(self):
        """"""
        pass

    def __call__(self, *args, **kwargs):
        """"""
        pass

    def __dir__(self):
        """"""
        pass

    def __format__(self, fmt):
        """"""
        pass

    def __hash__(self):
        """"""
        pass

    def __repr__(self):
        """"""
        pass

    def __sizeof__(self):
        """"""
        pass

    # type coercion

    def __str__(self):
        """"""
        pass

    def __bytes__(self):
        """"""
        pass

    def __bool__(self):
        """"""
        pass

    def __int__(self):
        """"""
        pass

    def __float__(self):
        """"""
        pass

    def __complex__(self):
        """"""
        pass

    def __index__(self):
        """"""
        pass

    # attribute access

    def __getattr__(self, attr):
        """"""
        pass

    def __setattr__(self, attr, value):
        """"""
        pass

    def __delattr__(self, attr):
        """"""
        pass

    # sequence methods

    def __contains__(self, value):
        """"""
        pass

    def __getitem__(self, item):
        """"""
        pass

    def __setitem__(self, item, value):
        """"""
        pass

    def __delitem__(self, item):
        """"""
        pass

    def __iter__(self):
        """"""
        pass

    def __len__(self):
        """"""
        pass

    def __length_hint__(self):
        """"""
        pass

    def __reversed__(self):
        """"""
        pass

    # unary operators (alphabetical)

    def __invert__(self):
        """"""
        pass

    def __neg__(self):
        """"""
        pass

    def __pos__(self):
        """"""
        pass

    # binary operators (alphabetical)

    def __add__(self, other):
        """"""
        pass

    def __and__(self, other):
        """"""
        pass

    def __divmod__(self, other):
        """"""
        pass

    def __eq__(self, other):
        """"""
        pass

    def __floordiv__(self, other):
        """"""
        pass

    def __ge__(self, other):
        """"""
        pass

    def __gt__(self, other):
        """"""
        pass

    def __le__(self, other):
        """"""
        pass

    def __lshift__(self, other):
        """"""
        pass

    def __lt__(self, other):
        """"""
        pass

    def __matmul__(self, other):
        """"""
        pass

    def __mod__(self, other):
        """"""
        pass

    def __mul__(self, other):
        """"""
        pass

    def __ne__(self, other):
        """"""
        pass

    def __or__(self, other):
        """"""
        pass

    def __pow__(self, other):
        """"""
        pass

    def __rshift__(self, other):
        """"""
        pass

    def __sub__(self, other):
        """"""
        pass

    def __truediv__(self, other):
        """"""
        pass

    def __xor__(self, other):
        """"""
        pass

    # other math

    def __abs__(self):
        """"""
        pass

    def __ceil__(self):
        """"""
        pass

    def __floor__(self):
        """"""
        pass

    def __round__(self, n):
        """"""
        pass

    def __trunc__(self):
        """"""
        pass
