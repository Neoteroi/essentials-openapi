from dataclasses import dataclass
from enum import Enum

import pytest

from openapidocs.common import (
    Serializer,
    normalize_dict,
    normalize_dict_factory,
    normalize_key,
)


class ExampleType(Enum):
    A = "a"
    B = "b"


def test_serializer_raises_for_unsupported_class():
    class A:
        pass

    with pytest.raises(TypeError):
        Serializer().to_json(A())


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("one", "one"),
        ("snake_case", "snakeCase"),
        ("snake_case_really", "snakeCaseReally"),
        (10, 10),
        (ExampleType.A, "a"),
    ],
)
def test_normalize_key(value, expected_result):
    assert normalize_key(value) == expected_result


def test_normalize_dict_factory():
    class A:
        def to_obj(self):
            return {"x": 1}

    values = [("a", A())]

    assert normalize_dict_factory(values) == {"a": {"x": 1}}


def test_normalize_dict_normal_dataclass():
    @dataclass
    class Foo:
        snake_case: str
        camelCase: int

    assert normalize_dict(Foo(snake_case="Python", camelCase=-1)) == {
        "snake_case": "Python",
        "camelCase": -1,
    }


def test_normalize_dict_class_with_dict_method():
    class Foo:
        def dict(self):
            return {"a": "Foo", "b": 500}

    assert normalize_dict(Foo()) == Foo().dict()
