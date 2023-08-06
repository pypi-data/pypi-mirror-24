from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

project_url = "https://github.com/lepisma/jrun"

setup(
    name="jrun",
    version="0.1.1",
    description="Run jupyter notebooks as command line scripts with variable overrides",
    long_description=readme,
    author="Abhinav Tushar",
    author_email="abhinav.tushar.vs@gmail.com",
    url=project_url,
    install_requires=[],
    keywords="",
    packages=find_packages(),
    entry_points={"console_scripts": ["jrun=jrun.cli:main"]},
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only"
    ))
