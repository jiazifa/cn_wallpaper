# -*- coding: utf-8 -*-
"""
Setup.py file
"""


import re
from setuptools import setup, find_packages

AUTHOR = "Tree"
EMAIL = "2332532718@qq.com"
URL = ""

NAME = "cn_wallpaper"
DESCRIPTION = """
A Tool
"""
REQUIRES_PYTHON = ">3.5"
REQUIRED: list = [
]

setup(
    name=NAME,
    version="0.1.0",
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages("src"),
    package_dir={"": "src"},

    include_package_data=True,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='MIT',
    entry_points={'console_scripts': ['paper = cn_wallpaper.cli:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)