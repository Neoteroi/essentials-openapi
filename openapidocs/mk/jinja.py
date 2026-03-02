"""
This module provides a Jinja2 environment.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Optional

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    select_autoescape,
)

from . import get_http_status_phrase, highlight_params, read_dict, sort_dict
from .common import DocumentsWriter, is_reference
from .md import normalize_link, write_table


def get_primary_type(type_val):
    """
    Returns the primary (first non-null) type from a schema type value.

    Handles both OAS 3.0 (string) and OAS 3.1 (list) type representations:
      - "string"             → "string"
      - ["string", "null"]   → "string"
      - ["null"]             → "null"
      - ["string", "integer"] → "string"
    """
    if not type_val:
        return None
    if isinstance(type_val, list):
        non_null = [t for t in type_val if t != "null"]
        return non_null[0] if non_null else "null"
    return type_val


def is_nullable_schema(schema) -> bool:
    """
    Returns True if the given schema is nullable.

    Handles both OAS 3.0 (nullable: true) and OAS 3.1 (type: [..., "null"]) patterns.
    """
    if not isinstance(schema, dict):
        return False
    if schema.get("nullable"):
        return True
    type_val = schema.get("type")
    if isinstance(type_val, list):
        return "null" in type_val
    return False


def get_type_display(type_val) -> str:
    """
    Returns a display string for a schema type value.

    Handles both OAS 3.0 (string) and OAS 3.1 (list) type representations:
      - "string"               → "string"
      - ["string", "null"]     → "string | null"
      - ["string", "integer"]  → "string | integer"
    """
    if not type_val:
        return ""
    if isinstance(type_val, list):
        return " | ".join(str(t) for t in type_val)
    return str(type_val)


def configure_filters(env: Environment):
    env.filters.update(
        {"route": highlight_params, "table": write_table, "link": normalize_link}
    )


def configure_functions(env: Environment):
    helpers = {
        "read_dict": read_dict,
        "sort_dict": sort_dict,
        "is_reference": is_reference,
        "scalar_types": {"string", "integer", "boolean", "number"},
        "get_http_status_phrase": get_http_status_phrase,
        "write_md_table": write_table,
        "get_primary_type": get_primary_type,
        "is_nullable_schema": is_nullable_schema,
        "get_type_display": get_type_display,
    }

    env.globals.update(helpers)


class OutputStyle(Enum):
    """
    Output style.
    """

    MKDOCS = 1
    """Markdown for MkDocs and PyMdown extensions"""

    MARKDOWN = 2
    """Basic Markdown"""

    PLANTUML_SCHEMAS = 100
    """PlantUML class diagram for components schemas."""

    PLANTUML_API = 101
    """PlantUML diagram of the API with request and response bodies."""


class PackageLoadingError(ValueError):
    def __init__(
        self, style: OutputStyle, templates_folder: str
    ) -> None:  # pragma: no cover
        super().__init__(
            f"Failed to read the templates for the output style {style.name}. "
            f"Tried to read templates from the folder: {__name__}.{templates_folder}. "
            "This is most probably an issue in `essentials-openapi`."
        )
        self.desired_style = style
        self.attempted_folder = templates_folder


def get_environment(
    package_name: str,
    views_style: OutputStyle = OutputStyle.MKDOCS,
    custom_templates_path: Optional[str] = None,
) -> Environment:
    templates_folder = f"views_{views_style.name}".lower()

    loaders = []

    # If custom templates path is provided, validate and add FileSystemLoader first
    if custom_templates_path:
        custom_path = Path(custom_templates_path)
        if not custom_path.exists():
            raise ValueError(
                f"Custom templates path does not exist: {custom_templates_path}"
            )
        if not custom_path.is_dir():
            raise ValueError(
                f"Custom templates path is not a directory: {custom_templates_path}"
            )
        loaders.append(FileSystemLoader(str(custom_path)))

    # Always add the package loader as fallback
    try:
        loaders.append(PackageLoader(package_name, templates_folder))
    except ValueError as package_loading_error:  # pragma: no cover
        if not custom_templates_path:
            raise PackageLoadingError(
                views_style, templates_folder
            ) from package_loading_error

    loader = ChoiceLoader(loaders)

    env = Environment(
        loader=loader,
        autoescape=select_autoescape(["html", "xml"])
        if os.environ.get("SELECT_AUTOESCAPE") in {"YES", "Y", "1"}
        else False,
        auto_reload=True,
        enable_async=False,
    )
    configure_filters(env)
    configure_functions(env)

    return env


class Jinja2DocumentsWriter(DocumentsWriter):
    """
    This class uses Jinja2 templating engine to generate other kinds of text output from
    source OpenAPI Documentation data.
    """

    def __init__(
        self,
        package_name: str,
        views_style: OutputStyle = OutputStyle.MKDOCS,
        custom_templates_path: Optional[str] = None,
    ) -> None:
        self._env = get_environment(package_name, views_style, custom_templates_path)

    @property
    def env(self) -> Environment:
        return self._env

    def get_template(self) -> Template:
        return self.env.get_template("layout.html")

    def write(self, data, **kwargs) -> str:
        template = self.get_template()
        return template.render(data, **kwargs)
