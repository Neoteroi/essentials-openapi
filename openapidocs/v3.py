"""
This module defines classes that can be used to generate OpenAPI Documentation
version 3.1.0.
https://swagger.io/specification/
"""
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from openapidocs.common import OpenAPIRoot, normalize_dict

from .common import OpenAPIElement


class ParameterLocation(Enum):
    """
    Defines possible locations where a parameter can be used in an OpenAPI specification.

    Attributes:
        QUERY: Parameter is passed as a query parameter in the URL.
        HEADER: Parameter is passed as a header in the request.
        PATH: Parameter is part of the URL path.
        COOKIE: Parameter is passed as a cookie.
    """

    QUERY = "query"
    HEADER = "header"
    PATH = "path"
    COOKIE = "cookie"


class ValueType(Enum):
    """
    Defines the possible data types for values in an OpenAPI specification.

    Attributes:
        ARRAY: Represents an array/list type.
        BOOLEAN: Represents a boolean type.
        INTEGER: Represents an integer type.
        NUMBER: Represents a number type (can be integer or float).
        OBJECT: Represents an object type.
        STRING: Represents a string type.
        NULL: Represents a null value.
    """

    ARRAY = "array"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"
    NULL = "null"


class ValueFormat(Enum):
    """
    Defines possible format specifiers for values in an OpenAPI specification.

    This enum provides standardized format values that can be used to further
    refine the basic data types defined in ValueType.

    Attributes:
        BASE64: Base64 encoded string.
        BINARY: Binary data.
        BYTE: Base64 encoded characters.
        DATE: A full date in ISO 8601 format (yyyy-MM-dd).
        DATETIME: Date and time in ISO 8601 format (yyyy-MM-ddTHH:mm:ssZ).
        TIME: Time in ISO 8601 format (HH:mm:ss).
        DURATION: Duration in ISO 8601 format.
        DOUBLE: Double precision floating point number.
        FLOAT: Single precision floating point number.
        INT32: Signed 32-bit integer.
        INT64: Signed 64-bit integer.
        PASSWORD: A hint to UIs to obscure input.
        EMAIL: Email address.
        IDNEMAIL: International email address.
        UUID: Universally unique identifier.
        PARTIALTIME: Partial time representation.
        HOSTNAME: Internet host name.
        IDNHOSTNAME: International host name.
        IPV4: IPv4 address.
        IPV6: IPv6 address.
        URI: Universal Resource Identifier.
        URIREFERENCE: URI reference.
        IRI: Internationalized Resource Identifier.
        IRIREFERENCE: IRI reference.
        URITEMPLATE: URI template.
        JSONPOINTER: JSON pointer.
        RELATIVEJSONPOINTER: Relative JSON pointer.
        REGEX: Regular expression.
    """

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
    """
    Defines the types of security schemes available in OpenAPI 3.1.

    Attributes:
        APIKEY: Security scheme using API keys.
        HTTP: Security scheme using HTTP authentication.
        OAUTH: Security scheme using OAuth 2.0.
        OAUTH2: Alternative name for OAuth 2.0 security scheme.
        OIDC: Security scheme using OpenID Connect.
        OPENIDCONNECT: Alternative name for OpenID Connect security scheme.
        MUTUALTLS: Security scheme using mutual TLS authentication.
    """

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
    """
    Represents external documentation in OpenAPI.

    Attributes:
        url (str): The URL for the external documentation.
        description (Optional[str]): A description of the external documentation.
    """

    url: str
    description: Optional[str] = None


@dataclass
class License(OpenAPIElement):
    """
    Represents a License object in OpenAPI.

    Attributes:
        name (str): The license name used for the API.
        identifier (Optional[str]): An SPDX license identifier.
        url (Optional[str]): A URL to the license used for the API.
    """

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
    """
    Represents a variable for server URL template substitution.

    Attributes:
        default (str): The default value to use for substitution, which SHALL be provided.
        description (Optional[str]): An optional description for the server variable.
        enum (Optional[List[str]]): An enumeration of string values to be used if the substitution options are limited to a specific set.
    """

    default: str
    description: Optional[str] = None
    enum: Optional[List[str]] = None


@dataclass
class Server(OpenAPIElement):
    """
    Represents a server serving the API.

    Attributes:
        url (str): A URL to the target host. This URL supports server variables and may be relative.
        description (Optional[str]): An optional string describing the host designated by the URL.
        variables (Optional[Dict[str, ServerVariable]]): A map between variable names and their definitions.
    """

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
    """
    Represents a discriminator for polymorphic schemas in OpenAPI.

    Attributes:
        property_name (str): The name of the property in the payload that will hold the discriminator value.
        mapping (Optional[Dict[str, str]]): An optional mapping from payload values to schema names or references.
    """

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
        additional_properties (Union[None, bool, "Schema", "Reference"]):
            Used to describe dictionaries. The additionalProperties keyword specifies
            the type of values in the dictionary. Values can be primitives (strings,
            numbers or boolean values), arrays or objects.
            https://swagger.io/docs/specification/v3_0/data-models/dictionaries/
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
        max_items (Optional[int]):
            The maximum number of items in an array.
        min_items (Optional[int]):
            The minimum number of items in an array.
        unique_items (Optional[bool]):
            Indicates if all items in an array must be unique.
        maximum (Optional[float]):
            The maximum value for numeric values.
        minimum (Optional[float]):
            The minimum value for numeric values.
        nullable (Optional[bool]):
            Indicates if the value can be null.
        pattern (Optional[str]):
            A regular expression pattern for string values.
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
    additional_properties: Union[None, bool, "Schema", "Reference"] = None
    default: Optional[Any] = None
    deprecated: Optional[bool] = None
    example: Any = None
    external_docs: Optional[ExternalDocs] = None
    ref: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content_encoding: Optional[str] = None
    content_media_type: Optional[str] = None
    pattern: Optional[str] = None
    max_length: Optional[float] = None
    min_length: Optional[float] = None
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
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
    """
    Represents a header object in OpenAPI.

    Attributes:
        description (Optional[str]): A description of the header.
        schema (Union[None, Schema, "Reference"]): The schema defining the type used for the header.
    """

    description: Optional[str] = None
    schema: Union[None, Schema, "Reference"] = None


@dataclass
class Example(OpenAPIElement):
    """
    Represents an example of a media type in OpenAPI.

    Attributes:
        summary (Optional[str]): Short summary of the example.
        description (Optional[str]): Detailed description of the example.
        value (Any): The embedded literal example. This field and external_value are mutually exclusive.
        external_value (Optional[str]): A URL that points to the literal example. This field and value are mutually exclusive.
    """

    summary: Optional[str] = None
    description: Optional[str] = None
    value: Any = None
    external_value: Optional[str] = None


@dataclass
class Reference(OpenAPIElement):
    """
    Represents a reference to another component in the OpenAPI specification.

    Attributes:
        ref (str): A reference string pointing to a component in the specification,
                  following the JSON Reference format.
        summary (Optional[str]): A short summary which by default should override that of the
                                referenced component.
        description (Optional[str]): A description which by default should override that of the
                                    referenced component.
    """

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
    """
    Represents an encoding definition for a specific media type in OpenAPI.

    Attributes:
        content_type (Optional[str]): The Content-Type for encoding specific parts of the request body.
        headers (Optional[Dict[str, Union[Header, Reference]]]): A map of headers that are sent with the encoding defined by content_type.
        style (Optional[str]): Describes how the parameter value will be serialized.
        explode (Optional[bool]): When style is form, the default value is true, otherwise the default value is false.
        allow_reserved (Optional[bool]): Determines whether the parameter value should allow reserved characters.
    """

    content_type: Optional[str] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None


@dataclass
class Link(OpenAPIElement):
    """
    Represents a Link object in OpenAPI which describes a possible design-time link for a response.

    Attributes:
        operation_ref (Optional[str]): A relative or absolute URI reference to an OAS operation.
        operation_id (Optional[str]): The name of an existing, resolvable OAS operation.
        parameters (Optional[Dict[str, Any]]): A map representing parameters to pass to the linked operation.
        request_body (Any): A literal value or expression to use as a request body when calling the target operation.
        description (Optional[str]): A description of the link.
        server (Optional[Server]): A server object to be used by the target operation.
    """

    operation_ref: Optional[str] = None
    operation_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    request_body: Any = None
    description: Optional[str] = None
    server: Optional[Server] = None


@dataclass
class MediaType(OpenAPIElement):
    """
    Represents a media type in OpenAPI which provides schema and examples for a particular media type.

    Attributes:
        schema (Union[None, Schema, Reference]): The schema defining the content of the request, response, or parameter.
        examples (Optional[Dict[str, Union[Example, Reference]]]): Examples of the media type with their values.
        encoding (Optional[Dict[str, Encoding]]): A map between property names and their encoding information.
    """

    schema: Union[None, Schema, Reference] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


@dataclass
class Response(OpenAPIElement):
    """
    Represents a response in an OpenAPI operation.

    Attributes:
        description (Optional[str]): A description of the response.
        headers (Optional[Dict[str, Union[Header, Reference]]]): A map of headers to be sent with the response.
        content (Optional[Dict[str, Union[MediaType, Reference]]]): A map containing descriptions of potential response payloads.
        links (Optional[Dict[str, Union[Link, Reference]]]): A map of operations that can be called from the response.
    """

    description: Optional[str] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, Union[MediaType, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None


@dataclass
class Parameter(OpenAPIElement):
    """
    Represents a parameter in an OpenAPI operation.

    Attributes:
        name (str): The name of the parameter.
        in_ (ParameterLocation): The location of the parameter (query, header, path, cookie).
        schema (Union[None, Schema, Reference]): The schema defining the type used for the parameter.
        content (Optional[Dict[str, MediaType]]): A map containing the representations for the parameter.
        description (Optional[str]): A brief description of the parameter.
        required (Optional[bool]): Determines whether this parameter is mandatory.
        deprecated (Optional[bool]): Specifies that a parameter is deprecated.
        allow_empty_value (Optional[bool]): Sets the ability to pass empty-valued parameters.
        example (Optional[Any]): Example of the parameter's potential value.
        examples (Optional[Dict[str, Union[Example, Reference]]]): Examples of the parameter's potential value.
    """

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
    """
    Represents a request body in an OpenAPI operation.

    Attributes:
        content (Dict[str, MediaType]): A map containing descriptions of potential request payloads.
        description (Optional[str]): A brief description of the request body.
        required (Optional[bool]): Determines whether the request body is required in the API call.
    """

    content: Dict[str, MediaType]
    description: Optional[str] = None
    required: Optional[bool] = None


@dataclass
class SecurityRequirement(OpenAPIElement):
    """
    Represents a security requirement in OpenAPI.

    Attributes:
        name (str): The name of the security scheme to use.
        value (List[str]): List of scope names required for the execution. Empty list means no scopes.
    """

    name: str
    value: List[str]

    def to_obj(self):
        return {self.name: self.value}


@dataclass
class Operation(OpenAPIElement):
    """
    Represents an operation in an OpenAPI path.

    Attributes:
        responses (Dict[str, Response]): The responses available for this operation.
        tags (Optional[List[str]]): Tags for API documentation control.
        summary (Optional[str]): A short summary of what the operation does.
        description (Optional[str]): A detailed explanation of the operation behavior.
        external_docs (Optional[ExternalDocs]): Additional external documentation.
        operation_id (Optional[str]): Unique string identifying the operation.
        parameters (Optional[List[Union[Parameter, Reference]]]): Parameters that are applicable for this operation.
        request_body (Union[None, RequestBody, Reference]): The request body applicable for this operation.
        callbacks (Optional[Dict[str, Union["Callback", Reference]]]): Callbacks that may be initiated by the API provider.
        deprecated (Optional[bool]): Declares this operation to be deprecated.
        security (Optional[List[SecurityRequirement]]): Security requirements for this operation.
        servers (Optional[List[Server]]): Servers that provide this operation.
    """

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
    """
    Represents a path item in an OpenAPI document.

    A PathItem describes the operations available on a single path. It can be directly accessed from
    an OpenAPI object's paths map, where each path is mapped to its associated PathItem object.

    Attributes:
        summary (Optional[str]): A short summary of what the path represents.
        ref (Optional[str]): Reference to another PathItem definition.
        description (Optional[str]): A detailed explanation of the path's behavior.
        get (Optional[Operation]): The GET operation for this path.
        put (Optional[Operation]): The PUT operation for this path.
        post (Optional[Operation]): The POST operation for this path.
        delete (Optional[Operation]): The DELETE operation for this path.
        options (Optional[Operation]): The OPTIONS operation for this path.
        head (Optional[Operation]): The HEAD operation for this path.
        patch (Optional[Operation]): The PATCH operation for this path.
        trace (Optional[Operation]): The TRACE operation for this path.
        servers (Optional[List[Server]]): Servers overriding the global servers for this path.
        parameters (Optional[List[Union[Parameter, Reference]]]): Parameters common to all operations on this path.
    """

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
    """
    Represents a callback in an OpenAPI document.

    A Callback is a map of runtime expressions to path item objects that define the
    operations that will be invoked when the callback is triggered by the API provider.

    Attributes:
        expression (str): The runtime expression that specifies when the callback should be
                          invoked, such as a URL pointing to a callback destination.
        path (Union[PathItem, Reference]): The path item object or reference that defines
                                          the operations available on the callback destination.
    """

    expression: str
    path: Union[PathItem, Reference]

    def to_obj(self):
        return {self.expression: normalize_dict(self.path)}


@dataclass
class OAuthFlow(OpenAPIElement):
    """
    Represents an OAuth flow configuration in OpenAPI.

    This class defines the configuration details for an OAuth 2.0 flow type, including
    available scopes and the authorization and token URLs needed for the flow.

    Attributes:
        scopes (Dict[str, str]): Map between scope names and their descriptions.
        authorization_url (Optional[str]): The authorization URL to be used for the flow.
                                          Required for implicit and authorizationCode flows.
        token_url (Optional[str]): The token URL to be used for the flow.
                                  Required for password, clientCredentials, and authorizationCode flows.
        refresh_url (Optional[str]): The URL to be used for obtaining refresh tokens.
    """

    scopes: Dict[str, str]
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None
    refresh_url: Optional[str] = None


@dataclass
class OAuthFlows(OpenAPIElement):
    """
    Represents the available OAuth flows in an OpenAPI security scheme.

    This class contains configuration details for different OAuth 2.0 flows that can be used
    for authorization. Each flow type has its own configuration requirements.

    Attributes:
        implicit (Optional[OAuthFlow]): Configuration for the OAuth Implicit flow.
        password (Optional[OAuthFlow]): Configuration for the OAuth Resource Owner Password Credentials flow.
        client_credentials (Optional[OAuthFlow]): Configuration for the OAuth Client Credentials flow.
        authorization_code (Optional[OAuthFlow]): Configuration for the OAuth Authorization Code flow.
    """

    implicit: Optional[OAuthFlow] = None
    password: Optional[OAuthFlow] = None
    client_credentials: Optional[OAuthFlow] = None
    authorization_code: Optional[OAuthFlow] = None


class SecurityScheme(OpenAPIElement, ABC):
    """Abstract security scheme"""


@dataclass
class HTTPSecurity(SecurityScheme):
    """
    Represents HTTP authentication security scheme in OpenAPI.

    This class defines HTTP security schemes such as Basic, Bearer, or other HTTP authentication methods.

    Attributes:
        scheme (str): The name of the HTTP authorization scheme to be used.
                      Values include "basic", "bearer", etc.
        type (SecuritySchemeType): The type of the security scheme, always HTTP for this class.
        description (Optional[str]): A description of the security scheme.
        bearer_format (Optional[str]): A hint to the client to identify how the bearer token is formatted.
                                      For example, "JWT" for JSON Web Tokens.
    """

    scheme: str
    type: SecuritySchemeType = SecuritySchemeType.HTTP
    description: Optional[str] = None
    bearer_format: Optional[str] = None


@dataclass
class APIKeySecurity(SecurityScheme):
    """
    Represents an API key security scheme in OpenAPI.

    This class defines how an API key can be used for authentication and authorization.
    API keys can be passed in different locations: as a query parameter, in a header,
    or in a cookie.

    Attributes:
        name (str): The name of the header, query parameter, or cookie parameter to be used.
        in_ (ParameterLocation): The location of the API key (header, query, or cookie).
        type (SecuritySchemeType): The type of the security scheme, always APIKEY for this class.
        description (Optional[str]): A description of the security scheme.
    """

    name: str
    in_: ParameterLocation
    type: SecuritySchemeType = SecuritySchemeType.APIKEY
    description: Optional[str] = None


@dataclass
class OAuth2Security(SecurityScheme):
    """
    Represents an OAuth 2.0 security scheme in OpenAPI.

    This class defines how OAuth 2.0 can be used for authentication and authorization.
    It supports different OAuth 2.0 flows such as implicit, password, client credentials,
    and authorization code.

    Attributes:
        flows (OAuthFlows): An object containing configuration details for the supported OAuth flows.
        type (SecuritySchemeType): The type of the security scheme, always OAUTH2 for this class.
        description (Optional[str]): A description of the security scheme.
    """

    flows: OAuthFlows
    type: SecuritySchemeType = SecuritySchemeType.OAUTH2
    description: Optional[str] = None


@dataclass
class OpenIdConnectSecurity(SecurityScheme):
    """
    Represents an OpenID Connect security scheme in OpenAPI.

    This class defines how OpenID Connect Discovery can be used for authentication and authorization.
    It uses an OpenID Connect Discovery URL to locate the OpenID Connect configuration.

    Attributes:
        open_id_connect_url (str): The URL to the OpenID Connect Discovery endpoint,
                                   typically ending with .well-known/openid-configuration.
        type (SecuritySchemeType): The type of the security scheme, always OPENIDCONNECT for this class.
        description (Optional[str]): A description of the security scheme.
    """

    open_id_connect_url: str
    type: SecuritySchemeType = SecuritySchemeType.OPENIDCONNECT
    description: Optional[str] = None


@dataclass
class MutualTLSSecurity(SecurityScheme):
    """
    Represents a Mutual TLS security scheme in OpenAPI.

    This class defines how mutual TLS (Transport Layer Security) can be used for authentication
    where both the client and server authenticate each other using X.509 certificates.

    Attributes:
        type (SecuritySchemeType): The type of the security scheme, always MUTUALTLS for this class.
        description (Optional[str]): A description of the security scheme.
    """

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
    """
    Represents a tag for API documentation control.

    Tags are used to group operations in the OpenAPI documentation, making the API
    documentation more organized and easier to navigate.

    Attributes:
        name (str): The name of the tag.
        description (Optional[str]): A short description of the tag.
        external_docs (Optional[ExternalDocs]): Additional external documentation for this tag.
    """

    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None


@dataclass
class Security(OpenAPIElement):
    """
    Represents security requirements in an OpenAPI document.

    This class defines the security mechanisms required by the API. It allows for specifying
    alternative security requirement objects that can be used.

    Attributes:
        requirements (List[SecurityRequirement]): List of security requirement objects that
                                                  define the security mechanisms for the API.
        optional (bool): When set to True, indicates that security is optional by adding an
                         empty security requirement at the beginning of the list.
    """

    requirements: List[SecurityRequirement]
    optional: bool = False

    def to_obj(self):
        items = [normalize_dict(item) for item in self.requirements]
        if self.optional:
            items.insert(0, {})
        return items


@dataclass
class OpenAPI(OpenAPIRoot):
    """
    Represents the root object of an OpenAPI 3.1 document.

    This is the main entry point for the OpenAPI specification. It combines information about the API,
    its paths, components, servers, security definitions, and other metadata.

    Attributes:
        openapi (str): The semantic version number of the OpenAPI Specification version.
        info (Optional[Info]): Metadata about the API.
        json_schema_dialect (str): The default value for the $schema keyword within Schema Objects contained
                                  within this OAS document.
        paths (Optional[Dict[str, PathItem]]): The available paths and operations for the API.
        servers (Optional[List[Server]]): An array of Server Objects that provide connectivity information
                                        to a target server.
        components (Optional[Components]): Holds various reusable schemas for the specification.
        tags (Optional[List[Tag]]): A list of tags used by the specification with additional metadata.
        security (Optional[Security]): A declaration of which security mechanisms can be used across the API.
        external_docs (Optional[ExternalDocs]): Additional external documentation.
        webhooks (Optional[Dict[str, Union[PathItem, Reference]]]): Webhook definitions that MAY be called by the API provider.
    """

    openapi: str = "3.1.0"
    info: Optional[Info] = None
    json_schema_dialect: str = "https://json-schema.org/draft/2020-12/schema"
    paths: Optional[Dict[str, PathItem]] = None
    servers: Optional[List[Server]] = None
    components: Optional[Components] = None
    tags: Optional[List[Tag]] = None
    security: Optional[Security] = None
    external_docs: Optional[ExternalDocs] = None
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
