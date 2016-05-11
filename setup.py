#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="loggly-python-handler",
    version='1.0.0',
    description="Python logging handler that sends messages to Loggly",
    keywords="loggly logging handler https",
    author="psquickitjayant",
    author_email="jayantvarshney018@gmail.com",
    url="https://github.com/psquickitjayant/loggly-python-handler/",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests-futures >= 0.9.4"
        "pytz >= 2014.7"
    ],
    include_package_data=True,
    platform='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ]
)
