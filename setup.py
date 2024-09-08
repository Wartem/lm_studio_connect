# setup.py

"""
Setup script for the lm_studio_connect package.
Handles the packaging and dependencies.
"""

from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="lm_studio_connect",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
