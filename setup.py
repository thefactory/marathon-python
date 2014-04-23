import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='marathon',
      version="0.1.0",
      description='Marathon Client Library',
      long_description="""Python interface to the Marathon REST API.""",
      author='Mike Babineau',
      author_email='michael.babineau@gmail.com',
      install_requires=open('requirements.txt').read().splitlines(),
      url='https://github.com/thefactory/marathon-python',
      packages=['marathon'],
      license='MIT',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      **extra
)