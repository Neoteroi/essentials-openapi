"""
This module defines classes that can be used to generate OpenAPI Documentation
version 2.
https://swagger.io/specification/v2/
"""

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Type

from openapidocs.common import OpenAPIRoot

from .common import OpenAPIElement


def get_ref(ref_type: str | Type[Any]) -> str:
    if isinstance(ref_type, str):
        return f"#/definitions/{ref_type}"
    return f"#/definitions/{ref_type.__name__}"


class ParameterLocation(Enum):
    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    FORM = "formData"
    BODY = "body"


class APIKeyLocation(Enum):
    QUERY = "query"
    HEADER = "header"


class ValueType(Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    FILE = "file"
    INTEGER = "integer"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"


class HeaderType(Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"


class ValueItemType(Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    STRING = "string"


class ValueFormat(Enum):
    BINARY = "binary"
    BYTE = "byte"
    DATE = "date"
    DATETIME = "date-time"
    DOUBLE = "double"
    FLOAT = "float"
    INT32 = "int32"
    INT64 = "int64"
    PASSWORD = "password"


class CollectionFormat(Enum):
    CSV = "csv"
    SSV = "ssv"
    TSV = "tsv"
    PIPES = "pipes"
    MULTI = "multi"


class SecuritySchemeType(Enum):
    BASIC = "basic"
    APIKEY = "apiKey"
    OAUTH = "oauth2"
    OAUTH2 = "oauth2"


class OAuthFlowType(Enum):
    IMPLICIT = "implicit"
    PASSWORD = "password"
    APPLICATION = "application"
    ACCESS_CODE = "accessCode"


@dataclass
class Contact(OpenAPIElement):
    name: str | None = None
    url: str | None = None
    email: str | None = None


@dataclass
class ExternalDocs(OpenAPIElement):
    url: str
    description: str | None = None


@dataclass
class License(OpenAPIElement):
    name: str
    url: str | None = None


@dataclass
class Info(OpenAPIElement):
    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = None
    contact: Contact | None = None
    license: License | None = None


@dataclass
class XML(OpenAPIElement):
    name: str | None = None
    namespace: str | None = None
    prefix: str | None = None
    attribute: bool | None = None
    wrapped: bool | None = None


@dataclass
class Discriminator(OpenAPIElement):
    property_name: str
    mapping: dict[str, str] | None = None


@dataclass
class Schema(OpenAPIElement):
    type: None | str | ValueType = None
    format: None | str | ValueFormat = None
    required: list[str] | None = None
    properties: dict[str, "Schema"] | None = None
    default: Any | None = None
    deprecated: bool | None = None
    example: Any = None
    external_docs: ExternalDocs | None = None
    ref: str | None = None
    title: str | None = None
    description: str | None = None
    max_length: float | None = None
    min_length: float | None = None
    maximum: float | None = None
    minimum: float | None = None
    nullable: bool | None = None
    xml: XML | None = None
    items: "Schema | None" = None
    enum: list[str] | None = None
    discriminator: Discriminator | None = None
    all_of: list["Schema | Reference"] | None = None
    any_of: list["Schema | Reference"] | None = None
    one_of: list["Schema | Reference"] | None = None
    not_: list["Schema | Reference"] | None = None


@dataclass
class Header(OpenAPIElement):
    type: HeaderType
    description: str | None = None
    format: str | None = None
    items: "Items | None" = None
    collection_format: CollectionFormat | None = None
    default: Any = None
    maximum: float | None = None
    minimum: float | None = None
    exclusive_maximum: bool | None = None
    exclusive_minimum: bool | None = None
    enum: list[str] | None = None
    max_length: int | None = None
    min_length: int | None = None
    pattern: str | None = None
    max_items: int | None = None
    min_items: int | None = None
    unique_items: bool | None = None
    multiple_of: float | None = None


@dataclass
class Example(OpenAPIElement):
    summary: str | None = None
    description: str | None = None
    value: Any | None = None
    external_value: str | None = None


@dataclass
class Reference(OpenAPIElement):
    ref: str

    def to_obj(self) -> dict[str, str]:
        return {"$ref": self.ref}


@dataclass
class Encoding(OpenAPIElement):
    content_type: str | None = None
    headers: dict[str, Header | Reference] | None = None
    style: str | None = None
    explode: bool | None = None
    allow_reserved: bool | None = None


@dataclass
class Response(OpenAPIElement):
    description: str
    headers: dict[str, Header | Reference] | None = None
    schema: Schema | None = None
    examples: dict[str, Any] | None = None


@dataclass
class Items(OpenAPIElement):
    type: ValueItemType
    format: ValueFormat | None = None
    items: "Items | None" = None
    collection_format: CollectionFormat | None = None
    default: str | None = None
    maximum: float | None = None
    minimum: float | None = None
    exclusive_maximum: bool | None = None
    exclusive_minimum: bool | None = None
    enum: list[str] | None = None
    max_length: int | None = None
    min_length: int | None = None
    pattern: str | None = None
    max_items: int | None = None
    min_items: int | None = None
    unique_items: bool | None = None
    multiple_of: float | None = None


@dataclass
class Parameter(OpenAPIElement):
    name: str
    in_: ParameterLocation
    type: ValueType | None = None
    format: ValueFormat | None = None
    items: Items | None = None
    collection_format: CollectionFormat | None = None
    schema: Schema | None = None
    description: str | None = None
    allow_empty_value: bool | None = None
    example: Any | None = None
    examples: dict[str, Example | Reference] | None = None
    default: str | None = None
    maximum: float | None = None
    minimum: float | None = None
    exclusive_maximum: bool | None = None
    exclusive_minimum: bool | None = None
    enum: list[str] | None = None
    max_length: int | None = None
    min_length: int | None = None
    pattern: str | None = None
    max_items: int | None = None
    min_items: int | None = None
    unique_items: bool | None = None
    multiple_of: float | None = None
    required: bool | None = None


@dataclass
class SecurityRequirement(OpenAPIElement):
    name: str
    value: list[str]

    def to_obj(self):
        return {self.name: self.value}


@dataclass
class Operation(OpenAPIElement):
    responses: dict[str, Response]
    tags: list[str] | None = None
    operation_id: str | None = None
    summary: str | None = None
    consumes: list[str] | None = None
    produces: list[str] | None = None
    schemes: list[str] | None = None
    description: str | None = None
    external_docs: ExternalDocs | None = None
    parameters: list[Parameter | Reference] | None = None
    deprecated: bool | None = None
    security: list[SecurityRequirement] | None = None


@dataclass
class PathItem(OpenAPIElement):
    ref: str | None = None
    get: Operation | None = None
    put: Operation | None = None
    post: Operation | None = None
    delete: Operation | None = None
    options: Operation | None = None
    head: Operation | None = None
    patch: Operation | None = None
    parameters: list[Parameter | Reference] | None = None


class SecurityScheme(OpenAPIElement, ABC):
    """Abstract security scheme"""


@dataclass
class BasicSecurity(SecurityScheme):
    type: SecuritySchemeType = SecuritySchemeType.BASIC
    description: str | None = None


@dataclass
class APIKeySecurity(SecurityScheme):
    name: str
    in_: APIKeyLocation
    type: SecuritySchemeType = SecuritySchemeType.APIKEY
    description: str | None = None


@dataclass
class OAuth2Security(SecurityScheme):
    flow: OAuthFlowType
    scopes: dict[str, str]
    authorization_url: str | None = None
    token_url: str | None = None
    type: SecuritySchemeType = SecuritySchemeType.OAUTH2
    description: str | None = None


@dataclass
class Tag(OpenAPIElement):
    name: str
    description: str | None = None
    external_docs: ExternalDocs | None = None


@dataclass
class OpenAPI(OpenAPIRoot):
    swagger: str = "2.0"
    info: Info | None = None
    host: str | None = None
    base_path: str | None = None
    schemes: list[str] | None = None
    consumes: list[str] | None = None
    produces: list[str] | None = None
    paths: dict[str, PathItem] | None = None
    definitions: dict[str, Schema] | None = None
    parameters: dict[str, Parameter] | None = None
    responses: dict[str, Response] | None = None
    security_definitions: dict[str, SecurityScheme] | None = None
    security: list[SecurityRequirement] | None = None
    tags: list[Tag] | None = None
    external_docs: ExternalDocs | None = None
