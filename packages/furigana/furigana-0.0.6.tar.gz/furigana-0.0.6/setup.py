#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='furigana', 
	version='0.0.6',
	description='''convert Kanji in Japanese into Kanji attached with Hiragana (Furigana(振り仮名)). 
        For example, "澱んだ街角" => "澱(よど)んだ街角(まちかど)" ''',
	long_description = long_description,
	author='Miki.Liu',
	author_email='mikimotoh@gmail.com',
	url='https://github.com/MikimotoH/furigana',
	packages=['furigana'],
	classifiers=[
	    # How mature is this project? Common values are
	    #   3 - Alpha
	    #   4 - Beta
	    #   5 - Production/Stable
	    'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: Japanese',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules', 
            'Topic :: Text Processing :: Linguistic',
	    ],
	keywords='Japanese Language Processing',
	)
