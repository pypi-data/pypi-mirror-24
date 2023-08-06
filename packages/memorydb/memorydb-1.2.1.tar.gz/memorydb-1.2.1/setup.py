from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
   with open('README.rst', 'w+') as f:
       f.write(long_description)       
except (IOError, ImportError):
   long_description = ''

from distutils.core import setup
setup(
    name = 'memorydb',
    packages = ['memorydb'],
    version = '1.2.1',
    description = 'Simple In-Memory Database for Python',
    long_description = long_description,
    author = 'David Betz',
    author_email = 'dfb@davidbetz.net',
    url = 'https://github.com/davidbetz/pymemorydb',
    keywords = ['database', 'in-memory database'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
