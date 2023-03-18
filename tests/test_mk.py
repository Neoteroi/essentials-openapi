from datetime import date

import pytest

from openapidocs.mk import get_http_status_phrase, read_dict
from openapidocs.mk.common import is_array_schema, is_object_schema
from openapidocs.mk.contents import JSONContentWriter
from openapidocs.mk.md import normalize_link


def test_get_http_status_phrase():
    assert get_http_status_phrase(200) == "OK"
    assert get_http_status_phrase("200") == "OK"
    assert get_http_status_phrase("foo") == ""


def test_is_array_schema():
    assert is_array_schema({}) is False
    assert is_array_schema(1) is False
    assert is_array_schema({"type": "array"}) is False
    assert is_array_schema({"type": "array", "items": {}}) is True


def test_read_dict_raises_for_non_dict_property():
    with pytest.raises(ValueError):
        read_dict({"x": 1}, "x", "a")


def test_read_dict_default():
    value = read_dict({"x": {}}, "x a", default=...)
    assert value is ...

    value = read_dict({"x": {"a": None}}, "", default=...)
    assert value is ...


def test_is_object_schema():
    assert is_object_schema(1) is False
    assert is_object_schema({}) is False
    assert is_object_schema({"type": "object", "properties": {}}) is True


def test_normalize_link_raises():
    with pytest.raises(ValueError):
        normalize_link(None)  # type: ignore

    with pytest.raises(ValueError):
        normalize_link("")


def test_content_writer_dates():
    writer = JSONContentWriter()

    expected_value = """
{
    "date": "1986-05-30"
}
    """.strip()

    value = writer.write({"date": date(1986, 5, 30)})

    assert value == expected_value
