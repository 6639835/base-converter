from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="comprehensive-base-converter",
    version="1.0.0",
    author="Base Converter Team",
    description="A comprehensive cross-platform base converter utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6639835/base-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required
    ],
    entry_points={
        "console_scripts": [
            "base-converter=src.cli:main",
        ],
    },
)
