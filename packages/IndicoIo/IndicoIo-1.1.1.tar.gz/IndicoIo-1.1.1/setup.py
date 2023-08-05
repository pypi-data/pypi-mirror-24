"""
Setup for indico apis
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="IndicoIo",
    version="1.1.1",
    packages=[
        "indicoio",
        "indicoio.text",
        "indicoio.image",
        "indicoio.multi",
        "indicoio.utils",
        "indicoio.custom",
        "indicoio.pdf",
        "indicoio.docx",
        "tests",
    ],
    description="""A Python Wrapper for indico. Use pre-built state of the art machine learning algorithms with a single line of code.""",
    license="MIT License (See LICENSE)",
    long_description=open("README.rst").read(),
    url="https://github.com/IndicoDataSolutions/indicoio-python",
    author="Alec Radford, Slater Victoroff, Aidan McLaughlin, Madison May, Anne Carlson",
    author_email="engineering@indico.io",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=[
        "six >= 1.3.0",
        "pillow >= 2.8.1"
    ],
    install_requires=[
        "requests >= 1.2.3",
        "six >= 1.3.0",
        "pillow >= 2.8.1",
        "mock >= 1.3.0, < 2.0.0",
        "futures >= 3.0.0"
    ]
)
