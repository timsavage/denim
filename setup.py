# coding=utf-8
import os
from setuptools import setup, find_packages
import denim


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='denim',
    version=denim.__version__,
    packages=find_packages(exclude=('tests', 'tests.*')),
    scripts=['bin/den'],

    install_requires=['fabric'],

    package_data={
        'denim.scaffold': ['templates/*.txt', 'templates/*/*.txt'],
    },

    # Metadata for PyPI
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='A Fabric deployment strategy for Python web applications.',
    license='BSD',
    url='http://bitbucket.org/timsavage/denim',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ]
)
