# -*- coding: utf-8 -*-
import re
from os import path
from setuptools import find_packages, setup

ROOT_DIR = path.abspath(path.dirname(__file__))

DESCRIPTION = 'Gatco-APIManager - APIManager for Gatco'
LONG_DESCRIPTION = open(path.join(ROOT_DIR, 'README.rst')).read()
VERSION = re.search(
    "__version__ = '([^']+)'",
    open(path.join(ROOT_DIR, 'vamanager', '__init__.py')).read()
).group(1)


setup(
    name='Vamanager',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/sevencentco/vamanager',
    author='VietAnh',
    author_email='sevencentco@gmail.com',
     classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3.9",
    include_package_data=True,
    install_requires=[],
    extras_require={},
    zip_safe=False,
    platforms='any',
    entry_points={
    "console_scripts": [
        "vamanager = vamanager.manager:main",
    ],
},
)