# -*- coding:utf-8 -*-
import sys

from setuptools import setup, find_packages

if sys.version_info < (2, 7):
    sys.exit('Sorry, Python < 2.7 is not supported')

setup(
    name='pyformatter',
    version='0.0.1',
    url='https://github.com/PureWhiteWu/pyformatter',
    maintainer='PureWhiteWu',
    maintainer_email='daniel48@126.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyYAML==3.12',
    ],
)
