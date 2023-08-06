# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="corextext",
    version="0.1.0",
    description="CorexText finds latent factors that explain the most multivariate mutual information in bag of words representation of documents.",
    license="AGPL-3.0",
    author="Greg Ver Steeg/Rob Brekelmans",
    author_email = "brekelma@usc.edu",
    url="https://github.com/gregversteeg/corex_topic.git",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
