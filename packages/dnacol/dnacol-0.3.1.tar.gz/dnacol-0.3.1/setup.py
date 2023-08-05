#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

#load version number (can't just import the package since we might miss requirements)
execfile('dnacol/version.py')

#load long description from readme
with open('README.rst') as f:
    long_description = f.read()

setup(
    name = __title__,
    version = __version__,
    packages = find_packages(),

    # metadata for upload to PyPI
    author = "Nils Koelling",
    author_email = "git@nk.gl",
    description = "Display FASTA/FASTQ/SAM/VCF files with colored DNA/RNA bases and quality scores in the terminal",
    long_description = long_description,
    license = "MIT",
    keywords = "dnacol rnacol rna dna quality phred color colour bases console terminal stdout",
    url = "https://github.com/koelling/dnacol/",
    download_url="https://github.com/koelling/dnacol/archive/v%s.tar.gz" % __version__,
    platforms=["any"],

    entry_points={
        'console_scripts': ['dnacol = dnacol.dnacol:main']
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)