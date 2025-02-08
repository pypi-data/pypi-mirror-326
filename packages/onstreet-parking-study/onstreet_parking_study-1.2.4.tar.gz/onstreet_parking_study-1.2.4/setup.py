#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lapin",
    version="1.2.4",
    author="Laurent Gauthier, Antoine Laurent",
    author_email="lgauthier@agencemobilitedurable.ca, alaurent@agencemobilitedurable.ca",
    description="LPR data analysis package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://statdemontreal.visualstudio.com/Analyse%20de%20mobilit%C3%A9%20LAPI/_git/rev_saint_denis",
    license="GPL-3.0+",
    packages=[
        "lapin",
        "lapin.configs",
        "lapin.constants",
        "lapin.core",
        "lapin.figures",
        "lapin.io",
        "lapin.models",
        "lapin.processing",
        "lapin.tools",
        "lapin.transactions",
    ],
    install_requires=[
        "adjusttext",
        "azure-core",
        "azure-cosmos",
        "contextily",
        "deprecated",
        "folium",
        "geoalchemy2",
        "geopandas==0.14.3",
        "geopy",
        "importlib_resources",
        "jellyfish",
        "mapclassify",
        "matplotlib",
        "momepy==0.7",
        "networkx",
        "numba",
        "numpy==1.26.4",
        "openpyxl",
        "osmium",
        "osmnx",
        "osrm-py",
        "pandas",
        "pathvalidate",
        "psycopg2",
        "pyodbc",
        "requests",
        "scikit-learn",
        "scipy",
        "seaborn",
        "sqlalchemy",
        "statsmodels",
        "unidecode",
        "xlrd",
    ],
)
