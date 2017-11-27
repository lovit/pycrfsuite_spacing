from description import __version__, __author__
from setuptools import setup, find_packages

setup(
   name='pycrfsuite_spacing',
   version=__version__,
   author=__author__,
   author_email='soy.lovit@gmail.com',
   url='https://github.com/lovit/',
   description='Pycrfsuite를 이용한 띄어쓰기 교정기\n(Spacing corrector using pycrfsuite)',
   long_description="""Pycrfsuite를 이용한 띄어쓰기 교정기. 
   template generator, feature transformer를 포함하여 손쉽게 띄어쓰기 교정기를 학습할 수 있도록 하였습니다.
   자세한 사용법은 https://github.com/lovit/pycrfsuite_spacing/에 있습니다.
  
   This package makes easy to use including (1) template geneartor and (2) feature transformer.
   For detailed tutorials, see the README file on https://github.com/lovit/pycrfsuite_spacing/""",
   install_requires=['python-crfsuite>=0.9.2'],
   keywords=['pycrfsuite', 'spacing corrector'],
   packages=find_packages()
)
