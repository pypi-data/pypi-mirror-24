#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='redis-rw-lock',
    version='1.0.3',
    license='MIT',
    description="Redis based Reader-Writer lock with Writer's priority.",
    long_description='',
    author='Swapnil S. Mahajan',
    author_email='swapnilsm@gmail.com',
    url='https://github.com/swapnilsm/redis-rw-lock',
    packages=['redis_rw_lock',],
    # package_dir={'': '.'},
    # py_modules=[splitext(basename(path))[0] for path in glob('redis_rw_lock/*.py')],
    # py_modules=['redis_rw_lock'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'redis', 'lock', 'rwlock'
    ],
    install_requires=[
        'redis>=2.10.0',
        'python-redis-lock>=3.2.0'
    ]
)
