#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read()


setup(
    name="Reportic",
    version="0.0.1",
    author="Eugen Maksymenko",
    author_email="eugen.maksymenko@gmx.de",
    description="A CLI Report tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/EMaksy/reportrick",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)
