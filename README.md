# flake8-level12 #

[![CircleCI](https://circleci.com/gh/level12/flake8-level12.svg?style=svg&circle-token=0603b577ca2816d66fffa0379e4bf15ab05a2310)](https://circleci.com/gh/level12/flake8-level12)
[![codecov](https://codecov.io/gh/level12/flake8-level12/branch/master/graph/badge.svg?token=dPEpA2ns8p)](https://codecov.io/gh/level12/flake8-level12)

Set of flake8 plugins for Level 12 internal use. As with other flake8 plugins, when this module is
installed in a virtual environment, the plugins will be enabled and can be selected/ignored the
same way other codes are.

## Plugins ##

- _mock_autospec_
  - __M100__: autospec keyword arg missing
  - __M101__: autospec keyword should be True
  - __M102__: spec_set keyword arg missing
  - __M103__: spec_set keyword should be True

## Development ##

Each plugin in this package should have tests: `pytest` is used as the test runner. To run `tox`,
install `pytest` and `pytest-cov`.

### Checklist for new plugins ###

- create plugin module in `flake8_level12`
  - plugin class must have `name` and `version` attributes
  - `version` may be imported from `flake8_level12.version`
- add tests in the `tests` folder
- add the plugin definition to `setup.py` as described in [flake8 docs](http://flake8.pycqa.org/en/latest/plugin-development/registering-plugins.html)
