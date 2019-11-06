import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="plcx",
    version=find_version("plcx", "__init__.py"),
    description="async PLC communication",
    long_description="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="async plc",
    url="https://github.com/Cognexa/plcx",
    author="Cognexa Solutions s.r.o.",
    author_email="info@cognexa.com",
    license="MIT",
    packages=["plcx", "plcx.bag", "plcx.comm", "plcx.tests", "plcx.utils",],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[line for line in open("requirements.txt", "r").readlines() if not line.startswith("#")],
)
