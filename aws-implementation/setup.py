from setuptools import setup, find_packages
from pathlib import Path

def get_requirements(file_path: str) -> list:
    """
    Reads the requirements from a file and returns them as a list.
    Filters out comments, empty lines, and editable installs.
    """
    requirements = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-e ") or line == "-e .":
                continue
            requirements.append(line)
    return requirements

setup(
    name="aws-implementation",
    version="0.1.0",
    author="Prashanth Reddy",
    author_email="prashanthreddy.aidev@gmail.com",
    description="A simple implementation of AWS services using Boto3",
    long_description="This package provides a simple implementation of AWS services using Boto3.",
    long_description_content_type="text/markdown",
    url="https://github.com/prshanthreddy/mlops",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
