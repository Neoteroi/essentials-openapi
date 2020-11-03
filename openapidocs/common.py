import copy
import json
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, List, Tuple

import yaml
from essentials.json import FriendlyEncoder


class Format(Enum):
    YAML = "YAML"
    JSON = "JSON"


class OpenAPIRoot:
    """Base class for a root OpenAPI Documentation"""


def normalize_key(key: Any) -> str:
    if isinstance(key, Enum):
        return key.value
    if not isinstance(key, str):
        return key
    first, *others = key.rstrip("_").split("_")
    return "".join([first.lower(), *map(str.title, others)])


def normalize_dict_factory(items: List[Tuple[Any, Any]]) -> Any:
    data = {}
    for key, value in items:
        if value is None:
            continue

        if hasattr(value, "to_obj"):
            value = value.to_obj()

        if key == "ref":
            data["$ref"] = value
            continue

        if isinstance(value, Enum):
            value = value.value
        data[normalize_key(key)] = value
    return data


# replicates the asdict method from dataclasses module, to support
# bypassing "asdict" on child properties when they implement a `to_obj`
# method: some entities require a specific shape when represented
def _asdict_inner(obj, dict_factory):
    if hasattr(obj, "to_obj"):
        return obj.to_obj()
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


def normalize_dict(obj):
    if hasattr(obj, "to_obj"):
        return obj.to_obj()
    return _asdict_inner(obj, dict_factory=normalize_dict_factory)


class Serializer:
    """
    Provides methods to serialize dataclasses to JSON and YAML.
    """

    def _get_item_dictionary(self, item: Any) -> Any:
        if hasattr(item, "to_obj"):
            assert callable(item.to_obj), "to_obj must be a method"
            return item.to_obj()
        if is_dataclass(item):
            return normalize_dict(item)
        raise TypeError("Expected a dataclass or a class having a `to_obj()` method.")

    def to_obj(self, item: Any) -> Any:
        return self._get_item_dictionary(item)

    def to_json(self, item: Any) -> str:
        return json.dumps(
            self.to_obj(item), indent=4, ensure_ascii=False, cls=FriendlyEncoder
        )

    def to_yaml(self, item: Any) -> str:
        rep = yaml.dump(
            self.to_obj(item), sort_keys=False, indent=4, allow_unicode=True
        )
        assert isinstance(rep, str)
        return rep
