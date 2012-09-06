import os
from setuptools import setup
import denim

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='denim',
    version=denim.__version__,
    url='http://bitbucket.org/timsavage/denim',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='A Fabric deployment strategy for Python web applications.',
#    long_description=read('README.rst'),
    packages=[
        'denim',
        'denim.django',
        'denim.package',
        'denim.scaffold',
        'denim.scm',
        'denim.service',
        'denim.webserver',
    ],
# Enable this once scaffolding support is more mature.
#    scripts=[
#        'bin/den',
#    ],
    requires=['fabric'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ]
)
