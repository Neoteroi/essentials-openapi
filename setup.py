from setuptools import setup

from openapidocs import VERSION


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="essentials-openapi",
    version=VERSION,
    description="Classes to generate OpenAPI Documentation v3 and v2, in JSON and YAML",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/essentials-openapi",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="openapi docs swagger api documentation v3 v2 json yaml Markdown",
    license="MIT",
    packages=[
        "openapidocs",
        "openapidocs.commands",
        "openapidocs.mk",
        "openapidocs.mk.v3",
        "openapidocs.utils",
    ],
    install_requires=[
        "PyYAML>=6",
        "essentials>=1.1.5",
        "dataclasses==0.7;python_version<'3.7'",
    ],
    extras_require={
        "full": ["click~=8.1.3", "Jinja2~=3.1.2", "rich~=12.6.0", "httpx<1"]
    },
    entry_points={
        "console_scripts": [
            "openapidocs=openapidocs.main:main",
            "oad=openapidocs.main:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
