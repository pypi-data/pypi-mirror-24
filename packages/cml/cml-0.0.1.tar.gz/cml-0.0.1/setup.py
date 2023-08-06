from setuptools import setup, find_packages

setup(
   name = 'cml',
   version = '0.0.1',
   description = 'just a simple test',
   license = 'MIT License',
   install_requires = ['cloud-ml-sdk>=0.2.12'],
   author = 'yjw',
   packages = find_packages(),
   platforms = 'any',
)
