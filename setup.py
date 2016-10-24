#!/usr/bin/env python
import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name='marathon',
    version='0.8.7',
    description='Marathon Client Library',
    long_description="""Python interface to the Mesos Marathon REST API.""",
    author='Mike Babineau',
    author_email='michael.babineau@gmail.com',
    install_requires=['requests>=2.0.0', 'sseclient'],
    url='https://github.com/thefactory/marathon-python',
    packages=['marathon', 'marathon.models'],
    license='MIT',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **extra
)
