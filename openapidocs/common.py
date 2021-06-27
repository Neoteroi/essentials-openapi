import base64
import copy
import json
from abc import ABC, abstractmethod
from dataclasses import asdict, fields, is_dataclass
from datetime import date, datetime, time
from enum import Enum
from typing import Any, List, Tuple
from uuid import UUID

import yaml
from essentials.json import FriendlyEncoder


class Format(Enum):
    YAML = "YAML"
    JSON = "JSON"


class OpenAPIElement:
    """Base class for all OpenAPI Elements"""


class OpenAPIRoot(OpenAPIElement):
    """Base class for a root OpenAPI Documentation"""


class ValueTypeHandler(ABC):
    @abstractmethod
    def normalize(self, value: Any) -> Any:
        """Normalizes a value of the given type into another type."""


class CommonBuiltInTypesHandler(ValueTypeHandler):
    def normalize(self, value: Any) -> Any:
        if isinstance(value, UUID):
            return str(value)

        if isinstance(value, Enum):
            return value.value

        if isinstance(value, time):
            return value.strftime("%H:%M:%S")

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")

        if isinstance(value, bytes):
            return base64.urlsafe_b64encode(value).decode("utf8")

        return value


TYPES_HANDLERS = [CommonBuiltInTypesHandler()]


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

        for handler in TYPES_HANDLERS:
            value = handler.normalize(value)

        data[normalize_key(key)] = value
    return data


def regular_dict_factory(items: List[Tuple[Any, Any]]) -> Any:
    data = {}
    for key, value in items:
        for handler in TYPES_HANDLERS:
            value = handler.normalize(value)

        data[key] = value
    return data


# replicates the asdict method from dataclasses module, to support
# bypassing "asdict" on child properties when they implement a `to_obj`
# method: some entities require a specific shape when represented
def _asdict_inner(obj, dict_factory):
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    if hasattr(obj, "to_obj"):
        return obj.to_obj()
    if isinstance(obj, OpenAPIElement):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    if is_dataclass(obj):
        return asdict(obj, dict_factory=regular_dict_factory)
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
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    if hasattr(obj, "to_obj"):
        return obj.to_obj()
    if isinstance(obj, OpenAPIElement):
        return _asdict_inner(obj, dict_factory=normalize_dict_factory)
    return asdict(obj, dict_factory=regular_dict_factory)


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
