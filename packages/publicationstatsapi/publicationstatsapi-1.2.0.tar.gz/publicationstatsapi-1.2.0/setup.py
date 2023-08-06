#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'thriftpy==0.3.1',
    'requests>=2.11.1'
]

tests_require = []

setup(
    name="publicationstatsapi",
    version="1.2.0",
    description="Library that implements the endpoints of the Access Stats API",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="Fabio Batalha",
    maintainer_email="fabio.batalha@scielo.org",
    url="http://github.com/scieloorg/processing",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    dependency_links=[],
    tests_require=tests_require+install_requires,
    test_suite='tests',
    install_requires=install_requires
)
