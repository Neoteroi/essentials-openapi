"""
This module provides a Jinja2 environment to
"""
from enum import Enum

from jinja2 import Environment, PackageLoader, Template, select_autoescape

from . import get_http_status_phrase, highlight_params, read_dict, sort_dict
from .common import DocumentsWriter, is_reference
from .md import normalize_link, write_table


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
    package_name: str, views_style: OutputStyle = OutputStyle.MKDOCS
) -> Environment:
    templates_folder = f"views_{views_style.name}".lower()

    try:
        loader = PackageLoader(package_name, templates_folder)
    except ValueError as package_loading_error:  # pragma: no cover
        raise PackageLoadingError(
            views_style, templates_folder
        ) from package_loading_error
    else:
        env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html", "xml"]),
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
    ) -> None:
        self._env = get_environment(package_name, views_style)

    @property
    def env(self) -> Environment:
        return self._env

    def get_template(self) -> Template:
        return self.env.get_template("layout.html")

    def write(self, data, **kwargs) -> str:
        template = self.get_template()
        return template.render(data, **kwargs)
