import os

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="DeadTrap",
    author="Chr0m0s0m3s",
    description="An OSINT tool to track down footprints of a phone number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chr0m0s0m3s/DeadTrap",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Security",
    ],
    install_requires=[
        "selenium",
        "bs4",
        "configobj",
        "requests",
    ],
    include_package_data=True,
    python_requires=">=3.0",
    entry_points={"console_scripts": ["deadtrap=deadtrap.__main__:main"]}
)
