#! /usr/bin/python
# coding: utf-8

import io
import os
import sys
from codecs import open
from setuptools import setup, find_packages, Command
from shutil import rmtree


# General Attributes and Requirements
NAME = 'getmagpi'
DESCRIPTION = 'A simple utility to synchronize free MagPi PDF content.'
URL = 'https://jnario.github.io/getmagpi/'
EMAIL = 'jose@nario.com',
AUTHOR = 'Jose Nario',
REQUIRED = ['requests', 'beautifulsoup4']

here = os.path.abspath(os.path.dirname(__file__))

# Long Description -- remember to add readme to MANIFEST.IN
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Version
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,

    # Packages (one or the other)
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=['getmagpi'],

    # entry_points={
    #     'console_scripts': [
    #         'getmagpi = getmagpi:main'
    #     ],
    # },
    install_requires=REQUIRED,
    include_package_date=True,
    license='MIT',
    keywords='magpi raspberrypi library',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: System :: Archiving :: Mirroring',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)