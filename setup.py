import os
from setuptools import setup

from pymaps.__init__ import __version__

pkg_data = {'': ['templates/*.j2',
                 'styles/*.txt',]}


pkgs = ['pymaps']

# Dependencies
with open('requirements.txt') as f:
    dependencies = f.readlines()
install_requires = [t.strip() for t in dependencies]


config = dict(
    name='pymaps',
    version=__version__,
    description='Make beautiful maps with Google Maps JS API and Python',
    long_description='',
    author='Rafael Alves Ribeiro',
    author_email='rafael.alves.ribeiro@gmail.com',
    url='https://github.com/rafpyprog/pygmaps.git',
    keywords='data visualization',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha'],
    packages=pkgs,
    package_data=pkg_data,
    license='License :: OSI Approved :: MIT License',
    install_requires=install_requires,
    include_package_data=True
)

setup(**config)
