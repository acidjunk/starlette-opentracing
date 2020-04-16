"""
Starlette-OpenTracing
---------------------

This extension provides simple integration of OpenTracing in Starlette applications.
"""
from setuptools import setup

version = open("VERSION").read().strip()
setup(
    name="Starlette-OpenTracing",
    version=version,
    url="http://github.com/acidjunk/starlette-opentracing",
    download_url="https://github.com/acidjunk/starlette-opentracing/tarball/" + version,
    license="Apache 2.0",
    author="René Dohmen",
    author_email="acidjunk@gmail.com",
    description="OpenTracing support for Starlette and FastApi applications",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    packages=["starlette_opentracing", "tests"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["starlette", "opentracing>=2.0,<3"],
    extras_require={
        "tests": [
            "black",
            "flake8",
            "flake8-quotes",
            "isort",
            "mock",
            "pre-commit",
            "pytest",
            "pytest-cov",
            "requests",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
