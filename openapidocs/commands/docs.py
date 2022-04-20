from typing import Union

import click

from openapidocs.logs import logger
from openapidocs.mk.generate import generate_document
from openapidocs.mk.jinja import OutputStyle


@click.command(name="gen-docs")
@click.option(
    "-s",
    "--source",
    help=(
        "Source of the OpenAPI Documentation file. "
        "This can be either a public URL or a path to a file."
    ),
    required=True,
)
@click.option(
    "-d",
    "--destination",
    help="Destination file path.",
    required=True,
)
@click.option(
    "-t",
    "--style",
    help="The style of the output.",
    required=False,
    default="MKDOCS",
    show_default=True,
)
def generate_documents_command(source: str, destination: str, style: Union[int, str]):
    """
    Generates other kinds of documents from source OpenAPI Documentation files.

    For example, to generate Markdown for MkDocs and PyMdown:

    $ openapidocs gen-docs -s source-openapi.json -d output.md

    JSON and YAML sources are supported.
    It is also possible to fetch the specification file from a public URL:

    $ openapidocs gen-docs -s https://.../source-openapi.json -d output.md

    For more information, refer to the documentation at
    https://github.com/Neoteroi/essentials-openapi
    """
    try:
        generate_document(source, destination, style)
    except KeyboardInterrupt:  # pragma: nocover
        logger.info("User interrupted")
        exit(1)
    except ValueError as value_error:
        logger.error(value_error)
        exit(2)


@click.command(name="list-styles")
def list_styles_command():
    """
    Displays the supported output styles on the screen.
    """
    try:
        for value in OutputStyle:
            logger.info("%s: %s", value.name, value.value)
    except KeyboardInterrupt:  # pragma: nocover
        logger.info("User interrupted")
        exit(1)
