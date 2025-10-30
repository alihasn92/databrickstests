"""
Setup configuration for Knauf Sales Analytics package
"""

from setuptools import setup, find_packages

setup(
    name="knauf_sales_analytics",
    version="0.1.0",
    author="Hassan Ali",
    author_email="alihasn92@gmail.com",
    description="Sales analytics processing for Knauf Data Platform 2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alihasn92/databrickstests/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyspark>=3.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sales-processor=main:main",
        ],
    },
)