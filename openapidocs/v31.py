"""
This module defines classes that can be used to generate OpenAPI Documentation
version 3.1.
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
    NULL = "null"


class ValueFormat(Enum):
    BASE64 = "base64"
    BINARY = "binary"
    BYTE = "byte"
    DATE = "date"
    DATETIME = "date-time"
    TIME = "time"
    DURATION = "duration"
    DOUBLE = "double"
    FLOAT = "float"
    INT32 = "int32"
    INT64 = "int64"
    PASSWORD = "password"
    EMAIL = "email"
    IDNEMAIL = "idn-email"
    UUID = "uuid"
    PARTIALTIME = "partial-time"
    HOSTNAME = "hostname"
    IDNHOSTNAME = "idn-hostname"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    URI = "uri"
    URIREFERENCE = "uri-reference"
    IRI = "iri"
    IRIREFERENCE = "iri-reference"
    URITEMPLATE = "uri-template"
    JSONPOINTER = "json-pointer"
    RELATIVEJSONPOINTER = "relative-json-pointer"
    REGEX = "regex"


class SecuritySchemeType(Enum):
    APIKEY = "apiKey"
    HTTP = "http"
    OAUTH = "oauth2"
    OAUTH2 = "oauth2"
    OIDC = "openIdConnect"
    OPENIDCONNECT = "openIdConnect"
    MUTUALTLS = "mutualTLS"


@dataclass
class Contact(OpenAPIElement):
    """
    Represents a Contact object in OpenAPI.

    Attributes:
        name (Optional[str]): The identifying name of the contact person/organization.
        url (Optional[str]): The URL pointing to the contact information.
        email (Optional[str]): The email address of the contact person/organization.
    """
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
    identifier: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Info(OpenAPIElement):
    """
    Represents the Info object in OpenAPI.

    Attributes:
        title (str): The title of the API.
        version (str): The version of the API.
        summary (Optional[str]): A short summary of the API.
        description (Optional[str]): A detailed description of the API.
        terms_of_service (Optional[str]): A URL to the terms of service for the API.
        contact (Optional[Contact]): Contact information for the API.
        license (Optional[License]): License information for the API.
    """
    title: str
    version: str
    summary: Optional[str] = None
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
    """
    Represents an XML object in OpenAPI.

    Attributes:
        name (Optional[str]): The name of the XML element.
        namespace (Optional[str]): The namespace of the XML element.
        prefix (Optional[str]): The prefix to be used for the XML element.
        attribute (Optional[bool]): Whether the property is an attribute.
        wrapped (Optional[bool]): Whether the array is wrapped.
    """
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
    """
    Represents a Schema object in OpenAPI.

    Attributes:
        type (Union[None, str, ValueType, List[Union[None, str, ValueType]]]):
            The type of the schema (e.g., string, object, array).
        format (Union[None, str, ValueFormat]):
            The format of the schema (e.g., date-time, uuid).
        required (Optional[List[str]]):
            A list of required property names.
        properties (Optional[Dict[str, Union["Schema", "Reference"]]]):
            A dictionary of property names to their schemas or references.
        default (Optional[Any]):
            The default value for the schema.
        deprecated (Optional[bool]):
            Indicates if the schema is deprecated.
        example (Any):
            An example value for the schema.
        external_docs (Optional[ExternalDocs]):
            Additional external documentation for the schema.
        ref (Optional[str]):
            A reference to another schema.
        title (Optional[str]):
            The title of the schema.
        description (Optional[str]):
            A description of the schema.
        content_encoding (Optional[str]):
            The content encoding for the schema.
        content_media_type (Optional[str]):
            The content media type for the schema.
        max_length (Optional[float]):
            The maximum length for string values.
        min_length (Optional[float]):
            The minimum length for string values.
        maximum (Optional[float]):
            The maximum value for numeric values.
        minimum (Optional[float]):
            The minimum value for numeric values.
        xml (Optional[XML]):
            Additional metadata for XML representation.
        items (Union[None, "Schema", "Reference"]):
            The schema for items in an array.
        enum (Optional[List[str]]):
            A list of allowed values for the schema.
        discriminator (Optional[Discriminator]):
            The discriminator for polymorphism.
        all_of (Optional[List[Union["Schema", "Reference"]]]):
            A list of schemas that must all apply.
        any_of (Optional[List[Union["Schema", "Reference"]]]):
            A list of schemas where at least one must apply.
        one_of (Optional[List[Union["Schema", "Reference"]]]):
            A list of schemas where exactly one must apply.
        not_ (Optional[List[Union["Schema", "Reference"]]]):
            A schema that must not apply.
    """
    type: Union[None, str, ValueType, List[Union[None, str, ValueType]]] = None
    format: Union[None, str, ValueFormat] = None
    required: Optional[List[str]] = None
    properties: Optional[Dict[str, Union["Schema", "Reference"]]] = None
    default: Optional[Any] = None
    deprecated: Optional[bool] = None
    example: Any = None
    external_docs: Optional[ExternalDocs] = None
    ref: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content_encoding: Optional[str] = None
    content_media_type: Optional[str] = None
    max_length: Optional[float] = None
    min_length: Optional[float] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
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
    summary: Optional[str] = None
    description: Optional[str] = None

    def to_obj(self) -> Dict[str, str]:
        obj = {"$ref": self.ref}
        if self.summary:
            obj["summary"] = self.summary
        if self.description:
            obj["description"] = self.description
        return obj


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
    description: Optional[str] = None
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
    summary: Optional[str] = None
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None
    operation_id: Optional[str] = None
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
    path: Union[PathItem, Reference]

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
class MutualTLSSecurity(SecurityScheme):
    type: SecuritySchemeType = SecuritySchemeType.MUTUALTLS
    description: Optional[str] = None


@dataclass
class Components(OpenAPIElement):
    """
    Represents the reusable components of an OpenAPI document.

    Attributes:
        schemas (Optional[Dict[str, Union[Schema, Reference]]]):
            A dictionary of reusable Schema Objects or references to them.
        responses (Optional[Dict[str, Union[Response, Reference]]]):
            A dictionary of reusable Response Objects or references to them.
        parameters (Optional[Dict[str, Union[Parameter, Reference]]]):
            A dictionary of reusable Parameter Objects or references to them.
        examples (Optional[Dict[str, Union[Example, Reference]]]):
            A dictionary of reusable Example Objects or references to them.
        request_bodies (Optional[Dict[str, Union[RequestBody, Reference]]]):
            A dictionary of reusable RequestBody Objects or references to them.
        headers (Optional[Dict[str, Union[Header, Reference]]]):
            A dictionary of reusable Header Objects or references to them.
        security_schemes (Optional[Dict[str, Union[SecurityScheme, Reference]]]):
            A dictionary of reusable SecurityScheme Objects or references to them.
        links (Optional[Dict[str, Union[Link, Reference]]]):
            A dictionary of reusable Link Objects or references to them.
        callbacks (Optional[Dict[str, Union[Callback, Reference]]]):
            A dictionary of reusable Callback Objects or references to them.
        path_items (Optional[Dict[str, Union[PathItem, Reference]]]):
            A dictionary of reusable PathItem Objects or references to them.
    """
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    request_bodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    security_schemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    callbacks: Optional[Dict[str, Union[Callback, Reference]]] = None
    path_items: Optional[Dict[str, Union[PathItem, Reference]]] = None


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
    openapi: str = "3.1.1"
    info: Optional[Info] = None
    json_schema_dialect: str = "https://json-schema.org/draft/2020-12/schema"
    paths: Optional[Dict[str, PathItem]] = None
    servers: Optional[List[Server]] = None
    components: Optional[Components] = None
    tags: Optional[List[Tag]] = None
    security: Optional[Security] = None
    external_docs: Optional[ExternalDocs] = None
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
