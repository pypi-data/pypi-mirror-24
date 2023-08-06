from setuptools import setup

from stalimet import __version__, __author__

setup(
   name="stalimet",
   version=__version__,
   packages=['stalimet'],
   install_requires=['nltk'],
   scripts=['stalimet_run'],
   author=__author__,
   author_email="mari.fomicheva@gmail.com, amalinovskiy@gmail.com",
   description="Machine translation quality metric based on IBM2 statistical alignment model",
   license="Apache License 2.0",
   keywords="machine translation quality metric",
   url="https://github.com/amalinovskiy/stalimet",
)