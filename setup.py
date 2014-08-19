import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='marathon',
      version="0.4.0",
      description='Marathon Client Library',
      long_description="""Python interface to the Mesos Marathon REST API.""",
      author='Mike Babineau',
      author_email='michael.babineau@gmail.com',
      install_requires=[ 'requests>=2.0.0' ],
      url='https://github.com/thefactory/marathon-python',
      packages=['marathon', 'marathon.models'],
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