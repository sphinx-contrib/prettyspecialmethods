import re

import pytest

from sphinxcontrib.prettyspecialmethods import SPECIAL_METHODS

# from https://raw.githubusercontent.com/python/cpython/3.8/Doc/reference/datamodel.rst
all_methods = {
    "__abs__",
    "__add__",
    "__aenter__",
    "__aexit__",
    "__aiter__",
    "__and__",
    "__anext__",
    "__await__",
    "__bool__",
    "__bytes__",
    "__call__",
    "__ceil__",
    "__class_getitem__",
    "__complex__",
    "__contains__",
    "__del__",
    "__delattr__",
    "__delete__",
    "__delitem__",
    "__dict__",
    "__dir__",
    "__divmod__",
    "__enter__",
    "__eq__",
    "__exit__",
    "__float__",
    "__floor__",
    "__floordiv__",
    "__format__",
    "__ge__",
    "__get__",
    "__getattr__",
    "__getattribute__",
    "__getitem__",
    "__gt__",
    "__hash__",
    "__iadd__",
    "__iand__",
    "__ifloordiv__",
    "__ilshift__",
    "__imatmul__",
    "__imod__",
    "__imul__",
    "__index__",
    "__init__",
    "__init_subclass__",
    "__int__",
    "__invert__",
    "__ior__",
    "__ipow__",
    "__irshift__",
    "__isub__",
    "__iter__",
    "__itruediv__",
    "__ixor__",
    "__le__",
    "__len__",
    "__length_hint__",
    "__lshift__",
    "__lt__",
    "__matmul__",
    "__missing__",
    "__mod__",
    "__mul__",
    "__ne__",
    "__neg__",
    "__new__",
    "__or__",
    "__pos__",
    "__pow__",
    "__radd__",
    "__rand__",
    "__rdivmod__",
    "__repr__",
    "__reversed__",
    "__rfloordiv__",
    "__rlshift__",
    "__rmatmul__",
    "__rmod__",
    "__rmul__",
    "__ror__",
    "__round__",
    "__rpow__",
    "__rrshift__",
    "__rshift__",
    "__rsub__",
    "__rtruediv__",
    "__rxor__",
    "__set__",
    "__set_name__",
    "__setattr__",
    "__setitem__",
    "__slots__",
    "__str__",
    "__sub__",
    "__truediv__",
    "__trunc__",
    "__xor__",
}

# not listed in the page above
all_methods |= {'__sizeof__'}


unimplemented_ops = dict(
    # not implemented
    inplace_ops={re.sub('^__', '__i', m) for m in all_methods} & all_methods,

    # typically redundant
    reverse_ops={re.sub('^__', '__r', m) for m in all_methods} & all_methods,

    # diffult to show clearly
    descriptor_ops={'__get__', '__set__', '__delete__', '__set_name__'},

    # unclear whether to apply the formatting to enter or exit
    with_ops={'__enter__', '__exit__'},
    async_with_ops={'__aenter__', '__aexit__'},

    # no aiter or anext builtin
    async_iter_ops={'__aiter__', '__anext__'},

    # difficult to represent
    other_ops={
        '__class_getitem__',
        '__del__',
        '__dict__',
        '__getattribute__',
        '__init__',
        '__init_subclass__',
        '__missing__',
        '__new__',
        '__slots__',
    },
)


@pytest.mark.parametrize("unimplemented", [
    pytest.param(v, id=k) for k, v in unimplemented_ops.items()
])
def test_not_implemented(unimplemented):
    """ Test that the sets above are accurate """
    assert all_methods & unimplemented == unimplemented
    assert SPECIAL_METHODS.keys() & unimplemented == set()


def test_lists_exhaustive():
    implemented = all_methods - set.union(*unimplemented_ops.values())
    assert set(SPECIAL_METHODS.keys()) == implemented
