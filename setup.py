from __future__ import with_statement
from setuptools import setup

setup(
    name='honk',
    version='0.4',
    description='Tool for dumping output of HTTP requests',
    url='https://github.com/ryantownshend/honk',
    author='Ryan Townshend',
    author_email='citizen.townshend@gmail.com',
    install_requires=[
        'click>=6.7',
        'click-log>=0.2.1',
        'PyYAML>=3.12',
        'tabulate>=0.8.2'
    ],
    py_modules=['honk'],
    entry_points={
        'console_scripts': [
            'honk = honk:main'
        ],
    },
)
