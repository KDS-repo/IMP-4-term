#!/usr/bin/env python

from platform import python_version_tuple

import setuptools


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if python_version_tuple()[0] < "3":
    raise ValueError("Error python version. Need python3 and more")

setup(
    name="dump",
    version="0.8.10",
    description="Dump function to YAML/JSON",
    author="Alex",
    url="https://github.com//DcDrugs/Serializator",
    license="MIT",
    setup_requires=["wheel"],
    install_requires=["pyyaml", "wheel"],
    packages=["tools", "libs/json", "libs/yaml", "factory", "application"],
    entry_points={"console_scripts": "dump=application.command_line:main"},
)
