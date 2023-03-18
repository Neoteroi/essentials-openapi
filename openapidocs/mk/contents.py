"""
This module contains classes to generate representations of content types by mime type.
"""
import os
from abc import ABC, abstractmethod
from datetime import datetime
from json import JSONEncoder
from urllib.parse import urlencode

from essentials.json import FriendlyEncoder, dumps


class OADJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return JSONEncoder.default(self, obj)
        except TypeError:
            if isinstance(obj, datetime):
                datetime_format = os.environ.get("OPENAPI_DATETIME_FORMAT")
                if datetime_format:
                    return obj.strftime(datetime_format)
                else:
                    return obj.isoformat()
            return FriendlyEncoder.default(self, obj)  # type: ignore


class ContentWriter(ABC):
    """
    Base type for classes that can create representations of request/response contents.
    """

    @abstractmethod
    def handle_content_type(self, content_type: str) -> bool:
        """
        Returns a value indicating whether this example handler can handle an example
        of the given type.
        """

    @abstractmethod
    def write(self, value) -> str:
        """
        Writes markdown to represent a value in a certain type of content.
        """


class JSONContentWriter(ContentWriter):
    def handle_content_type(self, content_type: str) -> bool:
        return "json" in content_type.lower()

    def write(self, value) -> str:
        return dumps(value, indent=4, cls=OADJSONEncoder)


class FormContentWriter(ContentWriter):
    def handle_content_type(self, content_type: str) -> bool:
        # multipart/form-data. Otherwise, use application/x-www-form-urlencoded.
        return "x-www-form-urlencoded" == content_type.lower()

    def write(self, value) -> str:
        return urlencode(value)
