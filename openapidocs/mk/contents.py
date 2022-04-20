"""
This module contains classes to generate representations of content types by mime type.
"""
import json
from abc import ABC, abstractmethod
from urllib.parse import urlencode


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
        return json.dumps(value, ensure_ascii=False, indent=4)


class FormContentWriter(ContentWriter):
    def handle_content_type(self, content_type: str) -> bool:
        # multipart/form-data. Otherwise, use application/x-www-form-urlencoded.
        return "x-www-form-urlencoded" == content_type.lower()

    def write(self, value) -> str:
        return urlencode(value)
