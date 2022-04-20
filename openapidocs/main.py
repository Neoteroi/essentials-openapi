import logging
import sys

import click

from openapidocs import VERSION
from openapidocs.commands.docs import generate_documents_command, list_styles_command
from openapidocs.logs import logger

sys.path.append(".")


@click.group()
@click.option(
    "--verbose", default=False, help="Whether to display debug output.", is_flag=True
)
@click.version_option(version=VERSION)
def main(verbose: bool):
    """
    Essentials OpenAPI CLI.

    https://github.com/Neoteroi/essentials-openapi
    """
    if verbose:  # pragma: nocover
        logger.setLevel(logging.DEBUG)

    logger.debug("Running in --verbose mode")


main.add_command(generate_documents_command)
main.add_command(list_styles_command)
