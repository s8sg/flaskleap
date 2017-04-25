from __future__ import absolute_import
import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('codegen/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='flask-codegen',
    description='Generate Flask code from Swagger docs',
    version=version,
    packages=['codegen'],
    package_data={'templates': ['codegen/templates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flask-codegen=codegen:generate'
        ]
    },
    install_requires=['PyYAML', 'click', 'jinja2', 'dpath', 'six'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
