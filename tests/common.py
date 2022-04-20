import json
import os
from typing import Any

import pkg_resources

from openapidocs.common import Format


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
        pkg_resources.resource_filename(__name__, os.path.join(".", "res", file_name)),
        mode="rt",
        encoding="utf8",
    ) as source:
        return source.read()


def get_file_json(file_name) -> Any:
    return json.loads(get_resource_file_content(file_name))
