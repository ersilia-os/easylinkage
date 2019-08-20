"""Setup file for the Python Record Linkage Toolkit."""

import os

from setuptools import find_packages, setup

def read(fname):
    """Read a file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="easylinkage",
    version="0.1.0",
    author="Miquel Duran-Frigola",
    author_email="miquelduranfrigola@gmail.com",

    platforms="any",

    # Description
    description="Easy record linkage for medical data",
    long_description=read('README.md'),

    packages=find_packages(
        exclude=["benchmarks", "docs",
                 "*.tests", "*.tests.*", "tests.*", "tests"]
    ),

    # Github
    url="https://github.com/miquelduranfrigola/easylinkage",

    python_requires=">=3.5",
    install_requires=[
        "recordlinkage>=0.13.2"
    ],
    license='BSD-3-Clause'
)