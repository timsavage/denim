from distutils.core import setup


setup(
    name='denim',
    version='0.1',
    url='http://bitbucket.org/timsavage/denim',
    author='Tim Savage',
    author_email='tim.savage@poweredbypenguins.org',
    description='A Fabric_ deployment strategy for Python web applications.',
    packages=[
        'denim',
        'denim.process_control',
        'denim.scm',
        'denim.webserver',
    ],
    requires=['fabric'],
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Framework :: Fabric',
    ]
)
