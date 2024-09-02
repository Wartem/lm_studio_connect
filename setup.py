from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="lm_studio_connect",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)