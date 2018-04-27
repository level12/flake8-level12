# flake8-level12 #

[![CircleCI](https://circleci.com/gh/level12/flake8-level12.svg?style=svg&circle-token=0603b577ca2816d66fffa0379e4bf15ab05a2310)](https://circleci.com/gh/level12/flake8-level12)
[![codecov](https://codecov.io/gh/level12/flake8-level12/branch/master/graph/badge.svg?token=dPEpA2ns8p)](https://codecov.io/gh/level12/flake8-level12)

Set of flake8 plugins designed for Level 12 internal use.

## Usage ##

This package is not currently published on PyPI, so the more direct git ref is needed:

    pip install git+https://github.com/level12/flake8-level12.git

As with other flake8 plugins, when this module is installed in a virtual environment, the plugins
will be enabled and can be selected/ignored the same way other codes are.

__Note__: if you have your project set up to check flake8 in tox, be sure to include this package in that test environment's `deps`.

## Plugins ##

- _mock_autospec_
  - The following patching usages are covered:
    - `mock.patch`, `mock.patch.object`, and `mock.patch.multiple`
    - usage as class/method decorator, or as a context manager
  - __M100__: autospec keyword arg missing
  - __M101__: autospec keyword should be True
  - __M102__: spec_set keyword arg missing
  - __M103__: spec_set keyword should be True

## Development ##

To develop on flake8-level12, begin by running our tests:

    git clone https://github.com/level12/flake8-level12 flake8-level12
    cd flake8-level12
    tox

As an alternative to using `tox`, you may run `pytest` from within your own virtual environment:

    pip install -e .[test]
    pytest

Each plugin in this package should have tests: `pytest` is used as the test runner.

### Checklist for new plugins ###

- create plugin module in `flake8_level12`
  - plugin class must have `name` and `version` attributes
  - `version` may be imported from `flake8_level12.version`
- add tests in the `tests` folder
- add the plugin definition to `setup.py` as described in [flake8 docs](http://flake8.pycqa.org/en/latest/plugin-development/registering-plugins.html)
