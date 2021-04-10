from setuptools import setup, find_packages

setup(
   name='sitebuilder',
   version='1.0',
   description='A module for building my personal website',
   author='David Laing',
   packages=find_packages(),
   scripts=['sitebuilder/bin/build_library', 'sitebuilder/bin/build_site'],
   install_requires=['bs4', 'pandas']
)