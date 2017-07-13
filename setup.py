from __future__ import with_statement
from setuptools import setup

setup(
    name='httpdumptool',
    version='0.1',
    description='Tool for dumping output of HTTP requests',
    url='https://github.com/ryantownshend/httpdumptool',
    author='Ryan Townshend',
    author_email='citizen.townshend@gmail.com',
    py_modules=['httpdumptool'],
    # install_requires=[
    #     'click>=6.6',
    #     'click-log>=0.1.4',
    # ],
    entry_points={
        'console_scripts': [
            'httpdumptool = httpdumptool:main',
        ],
    },
)
