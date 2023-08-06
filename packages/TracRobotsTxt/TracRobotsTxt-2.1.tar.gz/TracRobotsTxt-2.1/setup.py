#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 Noah Kantrowitz <noah@coderanger.net>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import os

from setuptools import setup

setup(
    name='TracRobotsTxt',
    version='2.1',
    packages=['robotstxt'],

    author='Noah Kantrowitz',
    author_email='noah@coderanger.net',
    description='Serve a robots.txt file from Trac.',
    long_description=open(os.path.join(
        os.path.dirname(__file__), 'README')).read(),
    license='3-Clause BSD',
    keywords='trac plugin robots',
    url='http://trac-hacks.org/wiki/RobotsTxtPlugin',
    download_url='http://trac-hacks.org/svn/robotstxtplugin/0.11#egg=TracRobotsTxt-dev',
    classifiers=[
        'Framework :: Trac',
        #'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent'
    ],

    install_requires=['Trac'],

    entry_points={
        'trac.plugins': [
            'robotstxt.web_ui = robotstxt.web_ui'
        ]
    }
)
