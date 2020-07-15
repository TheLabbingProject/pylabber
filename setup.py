from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.read().splitlines()
    install_requires = [
        requirement
        for requirement in requirements
        if not requirement.startswith("git+")
    ]
    dependency_links = [
        requirement
        for requirement in requirements
        if requirement.startswith("git+")
    ]

with open("requirements-dev.txt") as fh:
    dev_requirements = fh.read().splitlines()

setup(
    name="pylabber",
    version="0.1.0",
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
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={"dev": dev_requirements},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
