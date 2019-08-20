"""Setup file for the Python Record Linkage Toolkit."""

import os

from setuptools import find_packages, setup

import versioneer


def read(fname):
    """Read a file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="easylinkage",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Miquel Duran-Frigola",
    author_email="miquelduranfrigola@gmail.com",

    platforms="any",

    # Description
    description="Easy record linkage for medical data",
    long_description=read('README.md'),

    # Github
    url="https://github.com/miquelduranfrigola/easylinkage",

    python_requires=">=3.5",
    install_requires=[
        "recordlinkage>=0.13.2"
    ],
    license='BSD-3-Clause'
)