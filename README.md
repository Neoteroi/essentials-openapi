![Build](https://github.com/Neoteroi/essentials-openapi/workflows/Build/badge.svg)
[![pypi](https://img.shields.io/pypi/v/essentials-openapi.svg)](https://pypi.python.org/pypi/essentials-openapi)
[![versions](https://img.shields.io/pypi/pyversions/essentials-openapi.svg)](https://github.com/neoteroi/essentials-openapi)
[![license](https://img.shields.io/github/license/neoteroi/essentials-openapi.svg)](https://github.com/neoteroi/essentials-openapi/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/Neoteroi/essentials-openapi/branch/main/graph/badge.svg?token=WEZ8YECJDF)](https://codecov.io/gh/Neoteroi/essentials-openapi)

# essentials-openapi

Classes to generate OpenAPI Documentation v3 and v2, in JSON and YAML.

```bash
pip install essentials-openapi
```

## Useful links

* https://swagger.io/specification/
* https://editor.swagger.io

## Usage
This library has been created to implement generation of OpenAPI Documentation
in the [`BlackSheep` web framework](https://github.com/RobertoPrevato/BlackSheep).
This package contains only parts that belong logically to the OpenAPI specification,
and can be reused for other applications.

## Limitations

* Partial support for Parameter properties: `style` , `allow_reserved` ,
   `explode` are not handled
* Doesn't implement validation of values, currently it is only concerned in
   generating code from a higher level API (it might be extended in the future
   with classes for validation)
