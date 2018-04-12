from setuptools import setup


def get_version(fname='flake8_level12/version.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('version'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.md',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='flake8-level12',
    version=get_version(),
    description="Provides flake8 linters for Level 12",
    long_description=get_long_description(),
    keywords=['flake8', 'mock', 'autospec', 'testing'],
    author='Matt Lewellyn',
    author_email='matt.lewellyn@level12.io',
    url='https://github.com/level12/flake8-level12',
    py_modules=['flake8_level12'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'M10 = flake8_level12.mock_autospec:MockAutospecChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
