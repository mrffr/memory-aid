#!/usr/bin/env python3

import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='memory-aid-mrffr',
    version="0.0.3",
    description='CLI utility to aid in memorizing facts using spaced repetition.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='F Fitzgerald',
    url='https://github.com/mrffr/memory-aid',

    entry_points={
        'console_scripts': [
            'memory-aid = memory_aid.memory_aid:main',
            ],
        },

    # the directory name manually specified to avoid including tests
    packages=['memory_aid'], 
    # identifiers for pypi
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
