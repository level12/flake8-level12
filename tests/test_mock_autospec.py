import ast

import pytest

from flake8_level12.mock_autospec import MockAutospecChecker

ok_decorator_with_spec = '''
@mock.patch('foo',
            autospec=True, spec_set=True)
def bar(m_foo):
    pass
'''

ok_class_decorator_with_spec = '''
@mock.patch('foo', autospec=True, spec_set=True)
class Bar:
    def baz(self, m_foo):
        pass
'''

ok_direct_import = '''
@patch('foo', autospec=True, spec_set=True)
def bar(m_foo):
    pass
'''

ok_context_manager = '''
def foo():
    with mock.patch('bar', autospec=True, spec_set=True) as bar:
        pass
'''

ok_decorator_passes_value = '''
@mock.patch('foo', 'bar')
def baz():
    pass
'''

fail_decorator_missing_autospec = '''
@mock.patch('foo', spec_set=True)
def bar(m_foo):
    pass
'''

fail_class_decorator_missing_autospec = '''
@mock.patch('foo', spec_set=True)
class Bar:
    def baz(self, m_foo):
        pass
'''

fail_context_manager_missing_autospec = '''
def foo():
    with mock.patch('bar', spec_set=True) as bar:
        pass
'''

fail_decorator_wrong_autospec = '''
@mock.patch('foo', autospec=False, spec_set=True)
def bar(m_foo):
    pass
'''

fail_decorator_missing_spec_set = '''
@mock.patch('foo', autospec=True)
def bar(m_foo):
    pass
'''

fail_class_decorator_missing_spec_set = '''
@mock.patch('foo', autospec=True)
class Bar:
    def baz(self, m_foo):
        pass
'''

fail_decorator_wrong_spec_set = '''
@mock.patch('foo', autospec=True, spec_set=False)
def bar(m_foo):
    pass
'''


class TestMockAutospecChecker:
    @pytest.mark.parametrize(
        "code",
        [
            ok_decorator_with_spec,
            ok_class_decorator_with_spec,
            ok_decorator_passes_value,
            ok_context_manager,
            ok_direct_import,
        ]
    )
    def test_ok(self, code):
        tree = ast.parse(code)
        plugin = MockAutospecChecker(tree)
        assert not list(plugin.run())

    @pytest.mark.parametrize(
        "code,line,error",
        [
            (fail_decorator_missing_autospec, 2, 'M100'),
            (fail_class_decorator_missing_autospec, 2, 'M100'),
            (fail_decorator_wrong_autospec, 2, 'M101'),
            (fail_decorator_missing_spec_set, 2, 'M102'),
            (fail_class_decorator_missing_spec_set, 2, 'M102'),
            (fail_decorator_wrong_spec_set, 2, 'M103'),
            (fail_context_manager_missing_autospec, 3, 'M100'),
        ]
    )
    def test_single_fails(self, code, line, error):
        tree = ast.parse(code)
        plugin = MockAutospecChecker(tree)
        errors = list(plugin.run())
        assert len(errors) == 1
        assert errors[0][0] == line
        assert errors[0][2].split(' ')[0] == error