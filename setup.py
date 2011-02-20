#!/usr/bin/env python

METADATA = dict(
    name='python-panoramio',
    version='0.1',
    author='ramusus',
    description='Library for interacting with Panoramio Data API (http://www.panoramio.com/api/data/api.html)',
    long_description=open('README').read(),
    url='http://github.com/ramusus/python-panoramio',
)

if __name__ == '__main__':
    try:
        import setuptools
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)
