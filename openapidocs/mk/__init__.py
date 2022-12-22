"""
This module provides common functions to generate other kinds of representations from
source OpenAPI Documentation files.
"""
import re
from http import HTTPStatus

import markupsafe


def get_http_status_phrase(status_code) -> str:
    try:
        http_status = HTTPStatus(int(status_code))
        return http_status.phrase
    except ValueError:
        return ""


def read_dict(obj, *args, default=None):
    """
    Reads properties in a source dictionary, returning None if any

    Example:
    read_dict({"a": {"b": {"c": True}}}, "a", "b", "c") --> True
    """
    assert isinstance(obj, dict)

    value = obj
    for key in args:
        if not isinstance(value, dict):
            raise ValueError(f"Invalid sub-path: {repr(args)}")

        value = value.get(key)

        if value is None:
            return default

    if value is None or value is obj:
        return default

    return value


def sort_dict(obj):
    """
    Yields (key, value) of a dictionary with keys in alphabetical order.
    """
    for key in sorted(obj, key=str.lower):
        yield key, obj[key]


def highlight_params(path: str) -> str:
    def replacer(match):
        value = match.group()
        return f'<span class="route-param">{markupsafe.escape(value)}</span>'

    return re.sub(r"\{[^\}]+\}", replacer, path)
