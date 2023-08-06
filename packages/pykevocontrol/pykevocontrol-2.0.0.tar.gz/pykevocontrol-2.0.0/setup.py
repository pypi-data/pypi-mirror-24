from setuptools import setup
import os

setup(
    name = "pykevocontrol",
    version = "2.0.0",
    author = "Tristan Caulfield",
    author_email = "tcaulfld@gmail.com",
    description = "Control Kwikset Kevo locks",
    license = "MIT",
    keywords = "kevo kwikset",
    packages = ["pykevoplus"],
    url = "https://github.com/bahnburner/pykevoplus",
    long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    install_requires = [
        "requests",
        "beautifulsoup4"
    ]
)
