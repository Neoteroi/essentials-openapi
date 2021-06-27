"""
This module defines classes that can be used to generate OpenAPI Documentation
version 2.
https://swagger.io/specification/v2/
"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union

from openapidocs.common import OpenAPIRoot

from .common import OpenAPIElement


def get_ref(ref_type: Union[str, Type]) -> str:
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
    name: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None


@dataclass
class ExternalDocs(OpenAPIElement):
    url: str
    description: Optional[str] = None


@dataclass
class License(OpenAPIElement):
    name: str
    url: Optional[str] = None


@dataclass
class Info(OpenAPIElement):
    title: str
    version: str
    description: Optional[str] = None
    terms_of_service: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None


@dataclass
class XML(OpenAPIElement):
    name: Optional[str] = None
    namespace: Optional[str] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = None
    wrapped: Optional[bool] = None


@dataclass
class Discriminator(OpenAPIElement):
    property_name: str
    mapping: Optional[Dict[str, str]] = None


@dataclass
class Schema(OpenAPIElement):
    type: Union[None, str, ValueType] = None
    format: Union[None, str, ValueFormat] = None
    required: Optional[List[str]] = None
    properties: Optional[Dict[str, "Schema"]] = None
    default: Optional[Any] = None
    deprecated: Optional[bool] = None
    example: Any = None
    external_docs: Optional[ExternalDocs] = None
    ref: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    max_length: Optional[float] = None
    min_length: Optional[float] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    nullable: Optional[bool] = None
    xml: Optional[XML] = None
    items: Optional["Schema"] = None
    enum: Optional[List[str]] = None
    discriminator: Optional[Discriminator] = None
    all_of: Optional[List[Union["Schema", "Reference"]]] = None
    any_of: Optional[List[Union["Schema", "Reference"]]] = None
    one_of: Optional[List[Union["Schema", "Reference"]]] = None
    not_: Optional[List[Union["Schema", "Reference"]]] = None


@dataclass
class Header(OpenAPIElement):
    type: HeaderType
    description: Optional[str] = None
    format: Optional[str] = None
    items: Optional["Items"] = None
    collection_format: Optional[CollectionFormat] = None
    default: Any = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_maximum: Optional[bool] = None
    exclusive_minimum: Optional[bool] = None
    enum: Optional[List[str]] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
    multiple_of: Optional[float] = None


@dataclass
class Example(OpenAPIElement):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Any = None
    external_value: Optional[str] = None


@dataclass
class Reference(OpenAPIElement):
    ref: str

    def to_obj(self) -> Dict[str, str]:
        return {"$ref": self.ref}


@dataclass
class Encoding(OpenAPIElement):
    content_type: Optional[str] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None


@dataclass
class Response(OpenAPIElement):
    description: str
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    schema: Optional[Schema] = None
    examples: Optional[Dict[str, Any]] = None


@dataclass
class Items(OpenAPIElement):
    type: ValueItemType
    format: Optional[ValueFormat] = None
    items: Optional["Items"] = None
    collection_format: Optional[CollectionFormat] = None
    default: Optional[str] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_maximum: Optional[bool] = None
    exclusive_minimum: Optional[bool] = None
    enum: Optional[List[str]] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
    multiple_of: Optional[float] = None


@dataclass
class Parameter(OpenAPIElement):
    name: str
    in_: ParameterLocation
    type: Optional[ValueType] = None
    format: Optional[ValueFormat] = None
    items: Optional[Items] = None
    collection_format: Optional[CollectionFormat] = None
    schema: Optional[Schema] = None
    description: Optional[str] = None
    allow_empty_value: Optional[bool] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    default: Optional[str] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_maximum: Optional[bool] = None
    exclusive_minimum: Optional[bool] = None
    enum: Optional[List[str]] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
    multiple_of: Optional[float] = None
    required: Optional[bool] = None


@dataclass
class SecurityRequirement(OpenAPIElement):
    name: str
    value: List[str]

    def to_obj(self):
        return {self.name: self.value}


@dataclass
class Operation(OpenAPIElement):
    responses: Dict[str, Response]
    tags: Optional[List[str]] = None
    operation_id: Optional[str] = None
    summary: Optional[str] = None
    consumes: Optional[List[str]] = None
    produces: Optional[List[str]] = None
    schemes: Optional[List[str]] = None
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[SecurityRequirement]] = None


@dataclass
class PathItem(OpenAPIElement):
    ref: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None


class SecurityScheme(OpenAPIElement, ABC):
    """Abstract security scheme"""


@dataclass
class BasicSecurity(SecurityScheme):
    type: SecuritySchemeType = SecuritySchemeType.BASIC
    description: Optional[str] = None


@dataclass
class APIKeySecurity(SecurityScheme):
    name: str
    in_: APIKeyLocation
    type: SecuritySchemeType = SecuritySchemeType.APIKEY
    description: Optional[str] = None


@dataclass
class OAuth2Security(SecurityScheme):
    flow: OAuthFlowType
    scopes: Dict[str, str]
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None
    type: SecuritySchemeType = SecuritySchemeType.OAUTH2
    description: Optional[str] = None


@dataclass
class Tag(OpenAPIElement):
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None


@dataclass
class OpenAPI(OpenAPIRoot):
    swagger: str = "2.0"
    info: Optional[Info] = None
    host: Optional[str] = None
    base_path: Optional[str] = None
    schemes: Optional[List[str]] = None
    consumes: Optional[List[str]] = None
    produces: Optional[List[str]] = None
    paths: Optional[Dict[str, PathItem]] = None
    definitions: Optional[Dict[str, Schema]] = None
    parameters: Optional[Dict[str, Parameter]] = None
    responses: Optional[Dict[str, Response]] = None
    security_definitions: Optional[Dict[str, SecurityScheme]] = None
    security: Optional[List[SecurityRequirement]] = None
    tags: Optional[List[Tag]] = None
    external_docs: Optional[ExternalDocs] = None
