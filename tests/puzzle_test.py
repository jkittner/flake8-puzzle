import ast

import pytest

from flake8_puzzle import Plugin


def results(s):
    return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    's',
    (
        'my_func()',
        'my_func(123)',
        'my_func(foo="a string")',
        'var = "any/string/literal"',
        'my_function(var)',
        'my_function(f"something {var}")',
        'my_function("something {}".format(var))',
        'my_function(f"foo")',
        'my_function("foo", kwarg="bar")',
    ),
)
def test_invalid(s):
    assert not results(s)


@pytest.mark.parametrize(
    's',
    (
        'my_function("any/string/literal")',
        'my_function("and/string" "/literal")',
        'my_function("""anything""")',
        'a.b("foo")',
        'my_function(u"foo")',
    ),
)
def test_valid(s):
    msg, = results(s)
    assert msg == '1:0: PUZ6969 solved the puzzle!'
