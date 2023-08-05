#!/usr/bin/env python

from setuptools import setup

setup(
    name='py_zap',
    version='1.0.0',
    description='Python scraper for accessing ratings from tvbythenumbers.zap2it.com',
    author='sharibarboza',
    author_email='barbozashari@gmail.com',
    url='https://github.com/sharibarboza/py_zap',
    download_url='https://github.com/sharibarboza/py_zap/archive/1.0.0.tar.gz',
    keywords=['zap2it', 'ratings', 'tv'],
    license='MIT License',
    packages=['py_zap'],
    install_requires=[
        'beautifulsoup4',
        'requests>=2.9.1'
    ]
)