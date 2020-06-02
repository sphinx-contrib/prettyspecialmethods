import pytest


@pytest.mark.sphinx(testroot='simple', buildername='text')
def test_domain_py_objects(app, status, warning):
    app.builder.build_all()
    result = (app.outdir / 'index.txt').read_text()

    lines = [line.rstrip('\n') for line in result.splitlines() if line.strip()]

    assert lines == [
        'abs(self)',
        '*value* in *self*',
        'del *self*[*item*]',
        '*self*[*item*]',
        'hash(self)',
        '~*self*',
        'len(self)',
        '-*self*',
        '+*self*',
        'repr(self)',
        '*self*[*item*] = *value*',
        'str(self)',
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
    ]
