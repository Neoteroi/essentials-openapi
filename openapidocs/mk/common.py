"""
This module provides common functions that apply to all versions of the
OpenAPI Documentation specifications, when generating other kinds of representations
from source OAD files.
"""

from abc import ABC, abstractmethod


class DocumentsWriter(ABC):
    """
    Abstract class for types that can produce other kinds of text representations from
    source OpenAPI Documentation.
    """

    @abstractmethod
    def write(self, data, **kwargs) -> str:
        """
        Writes markdown.
        """


def is_reference(data) -> bool:
    """
    Returns a value indicating whether the given dictionary represents
    a reference.

    is_reference({"$ref": "..."}) -> True
    """
    if not isinstance(data, dict):
        return False
    return "$ref" in data


def is_object_schema(data) -> bool:
    """
    Returns a value indicating whether the given schema dictionary represents
    an object schema.

    is_reference({"type": "array", "items": {...}}) -> True
    """
    if not isinstance(data, dict):
        return False
    return data.get("type") == "object" and isinstance(data.get("properties"), dict)


def is_array_schema(data) -> bool:
    """
    Returns a value indicating whether the given schema dictionary represents
    an array schema.

    is_reference({"type": "array", "items": {...}}) -> True
    """
    if not isinstance(data, dict):
        return False
    return data.get("type") == "array" and isinstance(data.get("items"), dict)


def get_ref_type_name(reference) -> str:
    """
    Returns the type name of a reference.

    get_ref_type_name("#/components/schemas/Foo") -> "Foo"
    """
    if isinstance(reference, dict):
        reference = reference["$ref"]
    return reference.lstrip("#/").split("/")[-1]
