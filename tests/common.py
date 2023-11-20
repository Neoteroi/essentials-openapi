import json
import os
import re
from typing import Any

import yaml

from openapidocs.common import Format

try:
    from importlib.resources import files

    def get_resource_file_path(file_name: str) -> str:
        return str(files("tests") / "res" / file_name)

except ImportError:
    # Python 3.8
    import pkg_resources  # type: ignore

    def get_resource_file_path(file_name: str) -> str:
        return pkg_resources.resource_filename(
            __name__, os.path.join(".", "res", file_name)
        )


def debug() -> bool:
    return bool(os.environ.get("DEBUG", "1"))


def debug_result(version: str, instance: Any, result: str, format: Format) -> None:
    if not debug():
        return

    with open(
        f"{version}_debug_{instance.__class__.__name__}."
        f"{str(format.value).lower()}",
        mode="wt",
        encoding="utf8",
    ) as debug_file:
        debug_file.write(result)


def get_resource_file_content(file_name: str) -> str:
    with open(
        get_resource_file_path(file_name),
        mode="rt",
        encoding="utf8",
    ) as source:
        return source.read()


def get_file_json(file_name) -> Any:
    return json.loads(get_resource_file_content(file_name))


def get_file_yaml(file_name) -> Any:
    return yaml.safe_load(get_resource_file_content(file_name))


def normalize_str(value: str) -> str:
    return re.sub("\r?\n{2,}", "\n", value.strip())


def compatible_str(value_one: str, value_two: str) -> bool:
    """
    Compares two strings ignoring multiple carriage returns and trailing carriage
    returns. In HTML or Markdown it does not matter if you have multiple carriage
    returns.
    """
    # first check if the two strings are equals: there is no point in stripping carriage
    # returns otherwise
    if value_one == value_two:
        return True

    return normalize_str(value_one) == normalize_str(value_two)
