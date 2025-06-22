#!/usr/bin/env python3
"""
Setup script for AI Vision Pro
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-vision-pro",
    version="1.0.0",
    author="AI Vision Pro Team",
    author_email="contact@aivisionpro.com",
    description="Real-time object detection with professional web interface powered by YOLOv11",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ai-vision-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.8",
            "black>=21.0",
            "isort>=5.0",
        ],
        "gpu": [
            "torch>=1.9.0",
            "torchvision>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-vision-pro=run:main",
            "yodavi=src.yodavi:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    keywords="object-detection yolo computer-vision ai machine-learning flask",
    project_urls={
        "Bug Reports": "https://github.com/your-username/ai-vision-pro/issues",
        "Source": "https://github.com/your-username/ai-vision-pro",
        "Documentation": "https://github.com/your-username/ai-vision-pro/docs",
    },
)