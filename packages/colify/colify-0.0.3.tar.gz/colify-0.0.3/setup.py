from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='colify',
    version='0.0.3',
    description='Print arrays as columns',
    url='https://github.com/looneym/colify',
    author='Micheal Looney',
    license='MIT',
    keywords='print array column',
    packages=find_packages(),
)