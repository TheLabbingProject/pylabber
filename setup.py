import os
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("requirements.txt") as fh:
    requirements = fh.read().splitlines()

with open("requirements-dev.txt") as fh:
    dev_requirements = fh.read().splitlines()

setup(
    name="pylabber",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    scripts=["manage.py"],
    license="AGPLv3",
    description="A Django app to manage neuroscience research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheLabbingProject/pylabber",
    author="Zvi Baratz",
    author_email="baratzz@pm.me",
    keywords="django research neuroscience",
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
