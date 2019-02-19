import os
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="pylabber",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    scripts=["manage.py"],
    license="MIT",
    description="A Django app to manage neuroscience research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZviBaratz/pylabber",
    author="Zvi Baratz",
    author_email="z.baratz@gmail.com",
    keywords="django research neuroscience mri analysis",
    install_requires=["django"],
    extras_require={"dev": ["flake8", "yapf"], "test": ["pytest"]},
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
