from setuptools import setup
import setuptools

with open("README.md") as ld:
    long_description = ld.read()

setup(
    name="csinventory-py",
    version="0.1.1",
    author="Bmbus",
    description="Python package to get your Counter-Strike inventory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bmbus/csinventory-py/blob/master/setup.py",
    packages=setuptools.find_packages(),
    python_requires=">=3.7"
)