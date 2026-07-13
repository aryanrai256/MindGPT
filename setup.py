#!/usr/bin/env python3
"""
Setup script for MindCare Psychology Chatbot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mindcare-chatbot",
    version="1.0.0",
    author="MindCare Team",
    author_email="info@mindcare.example.com",
    description="A psychology and psychiatry chatbot for mental health support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/mindcare",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Sociology :: Psychology",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mindcare=main:main",
        ],
    },
    install_requires=[],  # No external dependencies
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "coverage>=5.0.0",
            "flake8>=3.0.0",
            "black>=21.0.0",
            "mypy>=0.900",
        ],
    },
)
