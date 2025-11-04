"""
This module provides methods to obtain OpenAPI Documentation from file or web sources.
"""

import json
from pathlib import Path
from typing import Any

import yaml

from openapidocs.logs import logger

from .web import ensure_success, http_get


def read_from_json_file(file_path: Path) -> dict[Any, Any] | list[Any]:
    """
    Reads JSON from a given file by path.
    """
    with open(file_path, "rt", encoding="utf-8") as source_file:
        return json.loads(source_file.read())


def read_from_yaml_file(file_path: Path) -> dict[Any, Any] | list[Any]:
    """
    Reads YAML from a given file by path.
    """
    with open(file_path, "rt", encoding="utf-8") as source_file:
        return yaml.safe_load(source_file.read())


class SourceError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def read_from_url(url: str) -> dict[Any, Any] | list[Any]:
    """
    Tries to read OpenAPI Documentation from the given source URL.
    This method will try to fetch JSON or YAML from the given source, in case of
    ambiguity regarding the content, it will to parse anyway the response as JSON or
    YAML (using safe load when handling YAML).
    """
    response = http_get(url)

    ensure_success(response)

    data = response.text
    content_type = response.headers.get("content-type")

    if "json" in content_type or url.endswith(".json"):
        return json.loads(data)

    if "yaml" in content_type or url.endswith(".yaml") or url.endswith(".yml"):
        return yaml.safe_load(data)

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        try:
            return yaml.safe_load(data)
        except yaml.YAMLError:
            raise SourceError(
                "Could not load a valid JSON or YAML file from the given URL."
            )


def read_from_source(
    source: str,
    cwd: Path | None = None,
) -> dict[Any, Any] | list[Any]:
    """
    Tries to read a JSON or YAML file from a given source.
    The source can be a path to a file, or a URL.

    Attempts to take from a relative path if `cwd` is provided.
    """
    potential_paths = [Path(source)]

    if cwd:
        potential_paths.append(cwd / source)

    for source_path in potential_paths:
        if source_path.exists():
            if not source_path.is_file():
                raise ValueError("The given path is not a file path.")

            logger.debug("Reading from file %s", source)

            file_path = source.lower()

            if file_path.endswith(".json"):
                return read_from_json_file(source_path)

            if file_path.endswith(".yaml") or file_path.endswith(".yml"):
                return read_from_yaml_file(source_path)
            else:
                raise ValueError("Unsupported source file.")
        else:
            logger.debug("Path %s does not exist, trying next.", source)

    source_lower = source.lower()

    if source_lower.startswith("http://") or source_lower.startswith("https://"):
        # fetch with a web request, read - ensure that it's JSON or YAML!
        return read_from_url(source)
    else:
        raise ValueError(
            "Invalid source: it must be either a path to a "
            ".json or .yaml file, or a valid URL."
        )
