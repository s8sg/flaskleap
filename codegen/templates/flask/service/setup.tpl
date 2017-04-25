#!/usr/bin/env python
import os
import sys
import pypandoc
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = pypandoc.convert_file('README.md', 'rst')


class PyTest(TestCommand):
    """class for py.test testing"""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.pytest_args = [
                ]

    def run_tests(self):
        import pytest
        err_no = pytest.main(self.pytest_args)
        sys.exit(err_no)


class PyTestWithCoverage(PyTest):
    """class for py.test testing with coverage generation and Validation"""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        coverage_goal = os.environ.get('COVERAGE_GOAL')
        if coverage_goal is None:
            coverage_goal = '80'
        self.pytest_args = [
                '--cov-report', 'xml',
                '--cov-config', '.coveragerc',
                '--cov', '{{ service_name }}',
                '--cov-fail-under', '%s' % coverage_goal
                ]

    def run_tests(self):
        import pytest
        err_no = pytest.main(self.pytest_args)
        sys.exit(err_no)


requirements = [
        "Flask>=0.2",
        "python-ldap",
        "flasgger",
        "watchdog"
        # "SQLAlchemy>=0.6",
        # "Flask-SQLAlchemy",
        # "sqlalchemy-migrate",
]

test_requirements = [
    "pytest",
    "pytest-cov",
    "python-ldap"
]


setup(
    name='{{ service_name }}',
    version='0.1.0',
    description='the {{ service_name }} service for Portal3',
    long_description=readme,
    author='s8sg',
    tests_require=test_requirements,
    cmdclass={
         'test': PyTest,
         'coverage': PyTestWithCoverage,
        },

    packages=find_packages(where=".", exclude=[".git", "test"]),
    setup_requires=[
        ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            '{{ service_name }}-service={{ service_name }}:run_app'
        ]
    },
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='{{ service_name }}',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite="test",
)
