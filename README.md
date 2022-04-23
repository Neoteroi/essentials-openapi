![Build](https://github.com/Neoteroi/essentials-openapi/workflows/Build/badge.svg)
[![pypi](https://img.shields.io/pypi/v/essentials-openapi.svg)](https://pypi.python.org/pypi/essentials-openapi)
[![versions](https://img.shields.io/pypi/pyversions/essentials-openapi.svg)](https://github.com/neoteroi/essentials-openapi)
[![license](https://img.shields.io/github/license/neoteroi/essentials-openapi.svg)](https://github.com/neoteroi/essentials-openapi/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Neoteroi/essentials-openapi/branch/main/graph/badge.svg?token=WEZ8YECJDF)](https://codecov.io/gh/Neoteroi/essentials-openapi)

# essentials-openapi

Classes to generate [OpenAPI Documentation](https://swagger.io/specification/)
v3 and v2, in JSON and YAML, and to generate other kinds of documents from
OpenAPI Documentation files.

```bash
pip install essentials-openapi
```

To install with dependencies to generate other kinds of artifacts from source
OpenAPI Documentation files:

```bash
pip install essentials-openapi[full]
```

## Useful links

* https://swagger.io/specification/
* https://editor.swagger.io

## Usage
This library has been originally created to implement generation of OpenAPI Documentation
in the [`BlackSheep` web framework](https://github.com/RobertoPrevato/BlackSheep).
However, this package is abstracted from that web framework and can be reused for other
applications. Today this library also offers functions to generate documentation from
source OpenAPI Documentation files.

## Features to generate artifacts from Open API Documentation

These require the full package: install it using `pip install essentials-openapi[full]`.

To generate output for [MkDocs](https://www.mkdocs.org) and [PyMdown extentions](https://facelessuser.github.io/pymdown-extensions/):

```bash
oad gen-docs -s example1-openapi.json -d output.md
```

![Example MkDocs documentation](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/06e157c4f49e27a7e488d72d36d199194e28e952/oad-example-1.png)

_Example of MkDocs documentation generated using [Neoteroi/mkdocs-plugins](https://github.com/Neoteroi/mkdocs-plugins)._

---

To generate a [PlantUML](https://plantuml.com) [class
diagram](https://plantuml.com/class-diagram) of the components schemas:

```bash
oad gen-docs -s source-openapi.json -d schemas.wsd --style "PLANTUML_SCHEMAS"
```

![Example schemas](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/06e157c4f49e27a7e488d72d36d199194e28e952/oad-example-schemas.png)

_Example of PlantUML diagram generated from components schemas._

---

To generate a [PlantUML](https://plantuml.com) [class
diagram](https://plantuml.com/class-diagram) with an overview of API endpoints:

```bash
oad gen-docs -s source-openapi.json -d schemas.wsd --style "PLANTUML_API"
```

![Example api overview](https://gist.githubusercontent.com/RobertoPrevato/38a0598b515a2f7257c614938843b99b/raw/3c6fdf85f6dd1a99ba1bd0486707dff557ff4ac4/oad-api-example.png)

_Example of PlantUML diagram generated from path items._

### Goals

* Provide an API to generate OpenAPI Documentation files.
* Providing functions to handle OpenAPI Documentation, like those to generate
  other kinds of documentation from source OpenAPI Documentation files.
* Support enough features to be useful for the most common API scenarios,
  especially for OAD files that are generated automatically from web frameworks.

### Non-Goals

* To implement the whole OAD Specification.
* For the features that generate artifacts: OpenAPI Documentation files are
  **supposed to be coming from trusted sources**. Trying to handle source files
  from untrusted sources and potentially causing HTML injection is out of the
  scope of this library.

## Limitations

* Partial support for Parameter properties: `style`, `allow_reserved`, `explode` are not
  handled.
* Doesn't implement validation of values, currently it is only concerned in generating
  code from a higher level API (it might be extended in the future with classes for
  validation).
* The features to generate artifacts from OpenAPI Documentation currently support only
  Version 3 of the specification.

### Styles

| Style            | Int value | Description                                  |
| ---------------- | --------- | -------------------------------------------- |
| MKDOCS           | 1         | Markdown for MkDocs and PyMdown extensions.  |
| MARKDOWN         | 2         | Basic Markdown.                              |
| HTML             | 3         | Plain HTML _(planned, not yet implemented)_. |
| PLANTUML_SCHEMAS | 100       | PlantUML schema for components schemas.      |
| PLANTUML_API     | 101       | PlantUML schema for API endpoints.           |

### Supported sources for OpenAPI Documentation

| Source                         | Example                                              |
| ------------------------------ | ---------------------------------------------------- |
| YAML file                      | `./docs/swagger.yaml`                                |
| JSON file                      | `./docs/swagger.json`                                |
| URL returning YAML on HTTP GET | `https://example-domain.net/swagger/v1/swagger.yaml` |
| URL returning JSON on HTTP GET | `https://example-domain.net/swagger/v1/swagger.json` |
