from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="essentials-openapi",
    version="0.1.1",
    description="Classes to generate OpenAPI Documentation v3 and v2, in JSON and YAML",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/neoteroi/essentials-openapi",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="openapi docs swagger api documentation v3 v2 json yaml",
    license="MIT",
    packages=["openapidocs"],
    install_requires=[
        "PyYAML==5.3.1",
        "essentials>=1.1.4",
        "dataclasses==0.7;python_version<'3.7'",
    ],
    include_package_data=True,
    zip_safe=False,
)
