#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 下午10:05
# @Author  : Hou Rong
# @Site    : 
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
    name='rate-limit-redis',
    version='0.1.0',
    license='MIT',
    description="A python rate limit tools, which have good compatibility for redis and gevent",
    author='Henry Hou',
    author_email='nmghr9@gmail.com',
    url='https://github.com/nmghr9/RateLimitRedis',
    install_requires=[
        'python-redis-lock',
    ],
    packages=find_packages(where='.', exclude=['']),
    zip_safe=False,
)
