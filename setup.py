#!/usr/bin/python3
import pathlib
import sys
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '0.1.8'
PACKAGE_NAME = 'thundera-bsa'
AUTHOR = 'Oscar Valenzuela B.'
AUTHOR_EMAIL = 'thunderabsa-pypi@amazon.com'
URL = 'https://github.com/amazon-ospo/thunderabsa-cli'
LICENSE = 'Apache-2.0'
DESCRIPTION = 'Command Line Interface for ThunderaBSA'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
      'click',
      'terminal_banner',
      'python-magic',
      'python-slugify',
      'binaryornot',
      'tabulate',
      'numpy',
      'lief',
      'demangler'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=['thundera', 'thundera.libs'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License'
    ],
    entry_points='''
        [console_scripts]
        thundera=thundera.thundera:cli
    ''',
)
