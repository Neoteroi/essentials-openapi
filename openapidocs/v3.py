"""
This module defines classes that can be used to generate OpenAPI Documentation
version 3.
https://swagger.io/specification/
"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from openapidocs.common import OpenAPIRoot, normalize_dict

from .common import OpenAPIElement


class ParameterLocation(Enum):
    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    COOKIE = "cookie"


class ValueType(Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"


class ValueFormat(Enum):
    BASE64 = "base64"
    BINARY = "binary"
    BYTE = "byte"
    DATE = "date"
    DATETIME = "date-time"
    DOUBLE = "double"
    FLOAT = "float"
    INT32 = "int32"
    INT64 = "int64"
    PASSWORD = "password"
    EMAIL = "email"
    UUID = "uuid"
    PARTIALTIME = "partial-time"


class SecuritySchemeType(Enum):
    APIKEY = "apiKey"
    HTTP = "http"
    OAUTH = "oauth2"
    OAUTH2 = "oauth2"
    OIDC = "openIdConnect"
    OPENIDCONNECT = "openIdConnect"


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
class ServerVariable(OpenAPIElement):
    default: str
    description: Optional[str] = None
    enum: Optional[List[str]] = None


@dataclass
class Server(OpenAPIElement):
    url: str
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariable]] = None


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
    properties: Optional[Dict[str, Union["Schema", "Reference"]]] = None
    default: Optional[Any] = None
    deprecated: Optional[bool] = None
    example: Any = None
    external_docs: Optional[ExternalDocs] = None
    ref: Optional[str] = None
    title: Optional[str] = None
    max_length: Optional[float] = None
    min_length: Optional[float] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    nullable: Optional[bool] = None
    xml: Optional[XML] = None
    items: Union[None, "Schema", "Reference"] = None
    enum: Optional[List[str]] = None
    discriminator: Optional[Discriminator] = None
    all_of: Optional[List[Union["Schema", "Reference"]]] = None
    any_of: Optional[List[Union["Schema", "Reference"]]] = None
    one_of: Optional[List[Union["Schema", "Reference"]]] = None
    not_: Optional[List[Union["Schema", "Reference"]]] = None


@dataclass
class Header(OpenAPIElement):
    description: Optional[str] = None
    schema: Union[None, Schema, "Reference"] = None


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
class Link(OpenAPIElement):
    operation_ref: Optional[str] = None
    operation_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    request_body: Any = None
    description: Optional[str] = None
    server: Optional[Server] = None


@dataclass
class MediaType(OpenAPIElement):
    schema: Union[None, Schema, Reference] = None
    example: Any = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


@dataclass
class Response(OpenAPIElement):
    description: Optional[str] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, Union[MediaType, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None


@dataclass
class Parameter(OpenAPIElement):
    name: str
    in_: ParameterLocation
    schema: Union[None, Schema, Reference] = None
    content: Optional[Dict[str, MediaType]] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    allow_empty_value: Optional[bool] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None


@dataclass
class RequestBody(OpenAPIElement):
    content: Dict[str, MediaType]
    required: Optional[bool] = None
    description: Optional[str] = None


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
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    request_body: Union[None, RequestBody, Reference] = None
    callbacks: Optional[Dict[str, Union["Callback", Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[SecurityRequirement]] = None
    servers: Optional[List[Server]] = None


@dataclass
class PathItem(OpenAPIElement):
    summary: Optional[str] = None
    ref: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None


@dataclass
class Callback(OpenAPIElement):
    expression: str
    path: PathItem

    def to_obj(self):
        return {self.expression: normalize_dict(self.path)}


@dataclass
class OAuthFlow(OpenAPIElement):
    scopes: Dict[str, str]
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None
    refresh_url: Optional[str] = None


@dataclass
class OAuthFlows(OpenAPIElement):
    implicit: Optional[OAuthFlow] = None
    password: Optional[OAuthFlow] = None
    client_credentials: Optional[OAuthFlow] = None
    authorization_code: Optional[OAuthFlow] = None


class SecurityScheme(OpenAPIElement, ABC):
    """Abstract security scheme"""


@dataclass
class HTTPSecurity(SecurityScheme):
    scheme: str
    type: SecuritySchemeType = SecuritySchemeType.HTTP
    description: Optional[str] = None
    bearer_format: Optional[str] = None


@dataclass
class APIKeySecurity(SecurityScheme):
    name: str
    in_: ParameterLocation
    type: SecuritySchemeType = SecuritySchemeType.APIKEY
    description: Optional[str] = None


@dataclass
class OAuth2Security(SecurityScheme):
    flows: OAuthFlows
    type: SecuritySchemeType = SecuritySchemeType.OAUTH2
    description: Optional[str] = None


@dataclass
class OpenIdConnectSecurity(SecurityScheme):
    open_id_connect_url: str
    type: SecuritySchemeType = SecuritySchemeType.OPENIDCONNECT
    description: Optional[str] = None


@dataclass
class Components(OpenAPIElement):
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    request_bodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    security_schemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    callbacks: Optional[Dict[str, Union[Callback, Reference]]] = None


@dataclass
class Tag(OpenAPIElement):
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None


@dataclass
class Security(OpenAPIElement):
    requirements: List[SecurityRequirement]
    optional: bool = False

    def to_obj(self):
        items = [normalize_dict(item) for item in self.requirements]
        if self.optional:
            items.insert(0, {})
        return items


@dataclass
class OpenAPI(OpenAPIRoot):
    openapi: str = "3.0.3"
    info: Optional[Info] = None
    paths: Optional[Dict[str, PathItem]] = None
    servers: Optional[List[Server]] = None
    components: Optional[Components] = None
    tags: Optional[List[Tag]] = None
    security: Optional[Security] = None
    external_docs: Optional[ExternalDocs] = None
