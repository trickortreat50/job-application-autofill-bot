"""
Setup script for Job Application Auto-Fill Bot
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="job-application-autofill-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An automated tool to fill out job application forms using browser automation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/job-application-autofill-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "job-autofill=main:main",
            "job-autofill-cli=main:run_cli_mode",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="job application automation selenium webdriver",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/job-application-autofill-bot/issues",
        "Source": "https://github.com/yourusername/job-application-autofill-bot",
        "Documentation": "https://github.com/yourusername/job-application-autofill-bot#readme",
    },
) 