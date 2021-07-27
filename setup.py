from setuptools import setup, find_packages #  find_packages will help in calling the libraries in the __init__ files and cache files

setup(
    name = 'src',
    version = '0.0.1',
    description = 'wine_mlops',
    author = 'Varun',
    packages = find_packages(),
    license = "MIT",
)