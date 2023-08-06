#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

__author__ = 'bac'

setup(
    name='sqlext',
    version='0.1',
    keywords=('sql', 'sqlalchemy', 'transaction', 'sql ext', 'render'),
    description=u'扩展了SqlAlchemy,支持声明式事务和手写SQL',
    license='Apache License',
    install_requires=['sqlalchemy'],

    url="http://xiangyang.li/project/python-sqlext",

    author='Shawn Li',
    author_email='shawn@xiangyang.li',

    packages=['sqlext'],
    platforms='any',
)
