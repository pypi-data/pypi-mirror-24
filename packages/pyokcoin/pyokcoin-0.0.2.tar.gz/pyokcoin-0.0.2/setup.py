#!/usr/bin/env python

from  setuptools import setup, find_packages

install_requires = ['requests']

setup(
    name='pyokcoin',
    packages=find_packages(),
    author_email = 'chiangqiqi@gmail.com',
    author='Alex Jiang',
    version='0.0.2',
    url = 'https://github.com/chiangqiqi/pyokcoin',
    download_url = 'https://github.com/chiangqiqi/pyokcoin/archive/0.0.2.tar.gz',
    description='okcoin simple restful api',
    install_requires=install_requires
)
