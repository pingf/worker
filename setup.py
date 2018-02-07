"""
worker
-------------

This is the description for that library
"""
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='worker',
    version='2018.02.04',
    url='https://github.com/pingf/worker.git',
    license='BSD',
    author='Jesse MENG',
    author_email='pingf0@gmail.com',
    description='store it',
    long_description=read('README.rst'),
    py_modules=['worker'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['worker'],
    zip_safe=False,
    include_package_data=True,
    # package_data={
    #     'worker': ['*'],  # All files from folder A
    # },
    platforms='any',
    install_requires=[
        'termcc', 'loader', 'async-timeout', 'aiohttp'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
