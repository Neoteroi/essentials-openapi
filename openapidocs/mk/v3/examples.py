"""
This module contains classes that are specific to the OpenAPI Documentation
Specification V3, to create examples of values from schemas. These are used to produce
basic examples of request and response bodies from schemas, when specific examples are
not included in documentation files.
"""
import random
from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Dict, Iterable, List, Type
from uuid import uuid4


class SchemaExampleHandler(ABC):
    """
    Base type for classes that can generate basic example values
    from schema types.
    """

    type_name: ClassVar[str]

    @abstractmethod
    def get_example(self, schema) -> Any:
        """
        Returns an example value for a property with the given name and schema.
        """


# TODO: allOf, anyOf, oneOf, not (?)
# https://swagger.io/docs/specification/data-models/oneof-anyof-allof-not/


class ScalarExampleHandler(SchemaExampleHandler):
    type_name = ""
    default: Any
    formats: Dict[str, Callable[[], Any]]

    def get_example(self, schema) -> str:
        format = schema.get("format")

        if format and format in self.formats:
            return self.formats[format]()

        return self.default


class StringExampleHandler(ScalarExampleHandler):
    type_name = "string"
    default = "string"
    formats = {
        "email": lambda: "derp@meme.org",
        "uuid": lambda: str(uuid4()),
        "date": lambda: "2022-04-13",
        "date-time": lambda: "2022-04-13T15:42:05.901Z",
        "password": lambda: "*" * 12,
        "byte": lambda: "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQ=",
        "binary": lambda: "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQ=",
    }

    def get_example(self, schema) -> str:
        enum = schema.get("enum")
        if isinstance(enum, list):
            return enum[0]
        return super().get_example(schema)


class IntegerExampleHandler(ScalarExampleHandler):
    type_name = "integer"
    default = 0
    formats = {
        "int32": lambda: random.randint(0, 300),
        "int64": lambda: random.randint(0, 300),
    }


class BooleanExampleHandler(ScalarExampleHandler):
    type_name = "boolean"
    default = True
    formats = {}


class NumberExampleHandler(ScalarExampleHandler):
    type_name = "number"
    default = 10.12
    formats = {
        "float": lambda: 10.12,
        "double": lambda: 10.12,
    }


class ObjectExampleHandler(SchemaExampleHandler):
    type_name = "object"

    def get_example(self, schema) -> Any:
        """
        Returns an example value for a property with the given name and schema.
        """
        properties = schema.get("properties") or {}

        example = {}

        for key in properties:
            example[key] = get_example_from_schema(properties[key])

        return example


class ArrayExampleHandler(SchemaExampleHandler):
    type_name = "array"

    def get_example(self, schema) -> Any:
        """
        Returns an example value for a property with the given name and schema.

        Example:
          type: array
          items:
            $ref: '#/components/schemas/ReleaseNodeDownload'
          nullable: true
        """
        items = schema["items"]
        return [get_example_from_schema(items) for _ in range(1)]


def get_subclasses(cls) -> Iterable[Type]:
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


def get_example_from_schema(schema) -> Any:
    if schema is None:
        return None

    if "example" in schema:
        return schema["example"]

    # does it have a type?
    handlers_types: List[Type[SchemaExampleHandler]] = list(
        get_subclasses(SchemaExampleHandler)
    )

    schema_type = schema.get("type")

    if schema_type:
        handler_type = next(
            (_type for _type in handlers_types if _type.type_name == schema_type), None
        )

        if handler_type is None:  # pragma: nocover
            # fallback to returning the raw schema;
            return schema

        handler = handler_type()
        return handler.get_example(schema)
    # TODO: handle special cases (allOf, anyOf, etc.)
    return None
