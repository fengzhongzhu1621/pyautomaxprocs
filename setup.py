# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import setup, find_packages

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
from setuptools import Command
from importlib import import_module


logger = logging.getLogger(__name__)

version = import_module('automaxprocs.version').version


class Tox(TestCommand):
    user_options = [('tox-args=', None, "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(args=self.tox_args.split())
        sys.exit(errno)


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


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


README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README, encoding='utf-8').read() + '\n\n'

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
        name='automaxprocs',
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
        keywords='xTool',
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
        setup_requires=[
            "flake8",
            'docutils>=0.14',
        ],
        extras_require={
            'dev': ['pytest'],
        },
        test_suite='tests',
        tests_require=test_requirements,
        cmdclass={'test': PyTest},
        # cmdclass={
        #     'test': Tox,
        #     'extra_clean': CleanCommand,
        # },
    )


if __name__ == "__main__":
    do_setup()
