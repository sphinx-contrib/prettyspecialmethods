import pytest


# SIMPLE_RESULT is shared among all tests as a check to ensure that
# all tests cover all supported special methods.
# Do not switch to separate values for each test without
# developing a replacement mechanism for ensuring this consistency.

# Non-method lines in result are prefixed with a hash (#)
# to allow for filtering

SIMPLE_RESULT = [
    '# misc (alphabetical)',
    'await *self*',
    '*self*(*args, **kwargs)',
    'dir(self)',
    'format(self, fmt)',
    'hash(self)',
    'repr(self)',
    'sys.getsizeof(self)',
    '# type coercion',
    'str(self)',
    'bytes(self)',
    'bool(self)',
    'int(self)',
    'float(self)',
    'complex(self)',
    'operator.index(self)',
    '# attribute access',
    'getattr(self, attr)',
    'setattr(self, attr, value)',
    'delattr(self, attr)',
    '# sequence methods',
    '*value* in *self*',
    '*self*[*item*]',
    '*self*[*item*] = *value*',
    'del *self*[*item*]',
    'iter(self)',
    'len(self)',
    'operator.length_hint(self)',
    'reversed(self)',
    '# unary operators (alphabetical)',
    '~*self*',
    '-*self*',
    '+*self*',
    '# binary operators (alphabetical)',
    '*self* + *other*',
    '*self* & *other*',
    'divmod(self, other)',
    '*self* == *other*',
    '*self* // *other*',
    '*self* >= *other*',
    '*self* > *other*',
    '*self* <= *other*',
    '*self* << *other*',
    '*self* < *other*',
    '*self* @ *other*',
    '*self* % *other*',
    '*self* * *other*',
    '*self* != *other*',
    '*self* | *other*',
    '*self* ** *other*',
    '*self* >> *other*',
    '*self* - *other*',
    '*self* / *other*',
    '*self* ^ *other*',
    '# other math',
    'abs(self)',
    'math.ceil(self)',
    'math.floor(self)',
    'round(self, n)',
    'math.trunc(self)',
]


@pytest.mark.sphinx(testroot='simple', buildername='text')
def test_domain_py_objects(app, status, warning):
    app.builder.build_all()
    result = (app.outdir / 'index.txt').read_text()

    lines = [line.rstrip('\n') for line in result.splitlines() if line.strip()]

    assert lines == SIMPLE_RESULT


@pytest.mark.sphinx(testroot='simple-self-param', buildername='text')
def test_domain_py_objects_with_self_param(app, status, warning):
    app.builder.build_all()
    result = (app.outdir / 'index.txt').read_text()

    lines = [line.rstrip('\n') for line in result.splitlines() if line.strip()]

    assert lines == [line.replace('self', 'obj') for line in SIMPLE_RESULT]


@pytest.mark.sphinx(testroot='autodoc', buildername='text')
def test_autodoc_module(app, status, warning):
    app.builder.build_all()
    result = (app.outdir / 'index.txt').read_text()

    lines = [line.strip() for line in result.splitlines() if line.strip()]

    expected = [line for line in SIMPLE_RESULT if not line.startswith('#')]
    expected.insert(0, 'class test_autodoc_module.MethodHolder')

    assert lines == expected


@pytest.mark.sphinx(testroot='autodoc-self-param', buildername='text')
def test_autodoc_module_with_self_param(app, status, warning):
    app.builder.build_all()
    result = (app.outdir / 'index.txt').read_text()

    lines = [line.strip() for line in result.splitlines() if line.strip()]

    expected = [
        line.replace('self', 'obj')
        for line in SIMPLE_RESULT
        if not line.startswith('#')
    ]
    expected.insert(0, 'class test_autodoc_self_param_module.MethodHolder')

    assert lines == expected
