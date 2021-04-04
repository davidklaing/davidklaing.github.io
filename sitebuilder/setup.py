from setuptools import setup

setup(
   name='sitebuilder',
   version='1.0',
   description='A module for building my personal website',
   author='David Laing',
   packages=['sitebuilder.library', 'sitebuilder.site'],
   scripts=['sitebuilder/bin/build_library'],
   install_requires=['click', 'pandas'],
)