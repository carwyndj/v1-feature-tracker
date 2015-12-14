"""setup.py: setuptools control."""
 
 
import re
from setuptools import setup, find_packages
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('v1_feature_tracker/v1_feature_tracker.py').read(),
    re.M
    ).group(1)
 
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "v1_feature_tracker",
    packages = ["v1_feature_tracker"],
    install_requires = ['v1pysdk-unofficial',
                        'xlsxwriter'],
    entry_points = {
        "console_scripts": ['v1_feature_tracker = v1_feature_tracker.v1_feature_tracker:main']
        },
    version = version,
    description = "Generate a v1 feature tracking Excel",
    long_description = long_descr,
    author = "Carwyn Jones",
    author_email = "carwyn.jones@nagra.com",
    url = "https://www.nagra.com",
    )