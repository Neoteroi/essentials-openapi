from typing import Union

from openapidocs.mk.v3 import OpenAPIV3DocumentationHandler
from openapidocs.utils.source import read_from_source


def generate_document(source: str, destination: str, style: Union[int, str]):
    # Note: if support for more kinds of OAD versions will be added, handle a version
    # parameter in this function

    data = read_from_source(source)
    handler = OpenAPIV3DocumentationHandler(data, style=style, source=source)

    html = handler.write()

    # TODO: support more kinds of destinations
    with open(destination, encoding="utf8", mode="wt") as output_file:
        output_file.write(html)
