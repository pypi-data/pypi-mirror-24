"""
Setup script
"""
from setuptools import setup, find_packages
from pypandoc import convert

REQUIRES = ['requests >= 2']

README = convert('README.md', 'rst')

setup(
    name='systranio',
    version='0.1.4',  # managed by bumbversion
    description='A simple REST API client for Systran.io',
    author='Canarduck',
    author_email='renaud@canarduck.com',
    url='https://github.com/canarduck/systran-translation-client',
    keywords=['Systran', 'Rest Translation API'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha', 'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ], )
