import ast

import pytest

from flake8_level12.numeric_column_prec import NumericPrecisionScaleChecker

ok_with_positional_args = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric(4, 2))
'''

ok_keyword_args = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric(precision=4, scale=2))
'''

ok_mixed_args = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric(4, scale=2))
'''


ok_no_import_alias = '''
import sqlalchemy

class Entity(db.Model):
    number = sqlalchemy.Column(sqlalchemy.Numeric(4, 2))
'''

ok_direct_import = '''
from sqlalchemy import Column, Numeric

class Entity(db.Model):
    number = Column(Numeric(4, 2))
'''

ok_not_sqlalchemy_numeric = '''
import sqlalchemy as sa
import foo

class Entity(db.Model):
    note = sa.Column(sa.Unicode)
    number = foo.Numeric()
'''

ok_other_functions = '''
def foo(*args):
    pass

x = 5

foo('abc')
foo(x)

'{}'.format(x)
foo(x)()
'''


fail_missing_both = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric())
'''

fail_no_alias = '''
import sqlalchemy

class Entity(db.Model):
    number = sqlalchemy.Column(sqlalchemy.Numeric())
'''


fail_direct_import = '''
from sqlalchemy import Column, Numeric

class Entity(db.Model):
    number = Column(Numeric())
'''

fail_class = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric)
'''

fail_class_direct_import = '''
from sqlalchemy import Column, Numeric

class Entity(db.Model):
    number = Column(Numeric)
'''

fail_missing_scale_positional = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric(4))
'''

fail_missing_precision = '''
import sqlalchemy as sa

class Entity(db.Model):
    number = sa.Column(sa.Numeric(scale=4))
'''


class TestNumericColumnChecker:
    @pytest.mark.parametrize('code', [
        ok_with_positional_args,
        ok_keyword_args,
        ok_mixed_args,
        ok_no_import_alias,
        ok_direct_import,
        ok_not_sqlalchemy_numeric,
        ok_other_functions,
    ])
    def test_ok(self, code):
        tree = ast.parse(code)
        plugin = NumericPrecisionScaleChecker(tree)
        assert not list(plugin.run())

    @pytest.mark.parametrize('code,line,expected_errors', [
        (fail_missing_both, 5, ['M110', 'M111']),
        (fail_no_alias, 5, ['M110', 'M111']),
        (fail_direct_import, 5, ['M110', 'M111']),
        (fail_class, 5, ['M110', 'M111']),
        (fail_class_direct_import, 5, ['M110', 'M111']),
        (fail_missing_scale_positional, 5, ['M111']),
        (fail_missing_precision, 5, ['M110']),
    ])
    def test_fail(self, code, line, expected_errors):
        tree = ast.parse(code)
        plugin = NumericPrecisionScaleChecker(tree)
        errors = list(plugin.run())
        assert len(errors) == len(expected_errors)
        for err, expect in zip(errors, expected_errors):
            assert err[0] == line
            assert err[2].split(' ')[0] == expect
