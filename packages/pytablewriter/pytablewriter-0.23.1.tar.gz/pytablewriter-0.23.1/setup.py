# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []


with io.open("README.rst", encoding=ENCODING) as f:
    long_description = f.read()

with io.open(
        os.path.join("docs", "pages", "introduction", "summary.txt"),
        encoding=ENCODING) as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="pytablewriter",
    version="0.23.1",
    url="https://github.com/thombashi/pytablewriter",

    author="Tsuyoshi Hombashi",
    author_email="tsuyoshi.hombashi@gmail.com",
    description=summary,
    include_package_data=True,
    install_requires=install_requires,
    keywords=[
        "table", "CSV", "Excel", "JavaScript", "JSON", "LTSV",
        "Markdown", "MediaWiki", "HTML", "pandas", "reStructuredText",
        "SQLite", "TSV", "TOML",
    ],
    license="MIT License",
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),

    setup_requires=pytest_runner,
    tests_require=tests_requires,
    extras_require={
        "test": tests_requires,
        "docs": docs_requires,
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
