import pytest
from enum import Enum
from openapidocs.common import Serializer, normalize_key, normalize_dict_factory


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
