# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import find_packages

import logging
import os
import codecs
import sys
from io import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools.command.test import test as TestCommand
from importlib import import_module


logger = logging.getLogger(__name__)

version = import_module('automaxprocs.version').version


def read(filename):
    """Read and return `filename` in root dir of project and return string ."""
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, filename), 'r').read()


test_requirements = [
    'pytest',
]


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


readme = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(readme, encoding='utf-8').read() + '\n\n'

install_requires = []
if os.path.exists("requirements.txt"):
    install_requires = read("requirements.txt").split()
    if "win" in sys.platform:
        for item in ['pexpect']:
            try:
                install_requires.remove(item)
            except ValueError as e:
                pass


install_requires.extend([

])


def do_setup():
    setup(
        name='pyautomaxprocs',
        version=version,
        description='Automatically get Linux container CPU quota like uber automaxprocs.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='jinyinqiao',
        author_email='jinyinqiao@gmail.com',
        license='MIT',
        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        install_requires=install_requires,
        zip_safe=False,
        scripts=None,
        keywords='automaxprocs',
        url='https://github.com/fengzhongzhu1621/automaxprocs',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Environment :: Console',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
        ],
        setup_requires=[],
        extras_require={
            'dev': ['pytest', 'bump2version'],
        },
        test_suite='tests',
        tests_require=test_requirements,
        cmdclass={'test': PyTest}
    )


if __name__ == "__main__":
    do_setup()
