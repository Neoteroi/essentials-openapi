import os
from typing import Any

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
