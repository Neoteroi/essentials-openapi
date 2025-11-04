"""
This module defines classes that can be used to generate OpenAPI Documentation
version 3.1.0.
https://swagger.io/specification/
"""

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any

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
        name (str | None): The identifying name of the contact person/organization.
        url (str | None): The URL pointing to the contact information.
        email (str | None): The email address of the contact person/organization.
    """

    name: str | None = None
    url: str | None = None
    email: str | None = None


@dataclass
class ExternalDocs(OpenAPIElement):
    """
    Represents external documentation in OpenAPI.

    Attributes:
        url (str): The URL for the external documentation.
        description (str | None): A description of the external documentation.
    """

    url: str
    description: str | None = None


@dataclass
class License(OpenAPIElement):
    """
    Represents a License object in OpenAPI.

    Attributes:
        name (str): The license name used for the API.
        identifier (str | None): An SPDX license identifier.
        url (str | None): A URL to the license used for the API.
    """

    name: str
    identifier: str | None = None
    url: str | None = None


@dataclass
class Info(OpenAPIElement):
    """
    Represents the Info object in OpenAPI.

    Attributes:
        title (str): The title of the API.
        version (str): The version of the API.
        summary (str | None): A short summary of the API.
        description (str | None): A detailed description of the API.
        terms_of_service (str | None): A URL to the terms of service for the API.
        contact (Contact | None): Contact information for the API.
        license (License | None): License information for the API.
    """

    title: str
    version: str
    summary: str | None = None
    description: str | None = None
    terms_of_service: str | None = None
    contact: Contact | None = None
    license: License | None = None


@dataclass
class ServerVariable(OpenAPIElement):
    """
    Represents a variable for server URL template substitution.

    Attributes:
        default (str): The default value to use for substitution, which SHALL be provided.
        description (str | None): An optional description for the server variable.
        enum (list[str] | None): An enumeration of string values to be used if the substitution options are limited to a specific set.
    """

    default: str
    description: str | None = None
    enum: list[str] | None = None


@dataclass
class Server(OpenAPIElement):
    """
    Represents a server serving the API.

    Attributes:
        url (str): A URL to the target host. This URL supports server variables and may be relative.
        description (str | None): An optional string describing the host designated by the URL.
        variables (dict[str, ServerVariable] | None): A map between variable names and their definitions.
    """

    url: str
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None


@dataclass
class XML(OpenAPIElement):
    """
    Represents an XML object in OpenAPI.

    Attributes:
        name (str | None): The name of the XML element.
        namespace (str | None): The namespace of the XML element.
        prefix (str | None): The prefix to be used for the XML element.
        attribute (bool | None): Whether the property is an attribute.
        wrapped (bool | None): Whether the array is wrapped.
    """

    name: str | None = None
    namespace: str | None = None
    prefix: str | None = None
    attribute: bool | None = None
    wrapped: bool | None = None


@dataclass
class Discriminator(OpenAPIElement):
    """
    Represents a discriminator for polymorphic schemas in OpenAPI.

    Attributes:
        property_name (str): The name of the property in the payload that will hold the discriminator value.
        mapping (dict[str, str] | None): An optional mapping from payload values to schema names or references.
    """

    property_name: str
    mapping: dict[str, str] | None = None


@dataclass
class Schema(OpenAPIElement):
    """
    Represents a Schema object in OpenAPI.

    Attributes:
        type (None | str | ValueType | List[None | str | ValueType]):
            The type of the schema (e.g., string, object, array).
        format (None | str | ValueFormat):
            The format of the schema (e.g., date-time, uuid).
        required (list[str] | None):
            A list of required property names.
        properties (dict[str, "Schema" | "Reference"] | None):
            A dictionary of property names to their schemas or references.
        additional_properties (None | bool | "Schema" | "Reference"):
            Used to describe dictionaries. The additionalProperties keyword specifies
            the type of values in the dictionary. Values can be primitives (strings,
            numbers or boolean values), arrays or objects.
            https://swagger.io/docs/specification/v3_0/data-models/dictionaries/
        default (Any | None):
            The default value for the schema.
        deprecated (bool | None):
            Indicates if the schema is deprecated.
        example (Any | None):
            An example value for the schema.
        external_docs (ExternalDocs | None):
            Additional external documentation for the schema.
        ref (str | None):
            A reference to another schema.
        title (str | None):
            The title of the schema.
        description (str | None):
            A description of the schema.
        content_encoding (str | None):
            The content encoding for the schema.
        content_media_type (str | None):
            The content media type for the schema.
        max_length (float | None):
            The maximum length for string values.
        min_length (float | None):
            The minimum length for string values.
        max_items (int | None):
            The maximum number of items in an array.
        min_items (int | None):
            The minimum number of items in an array.
        unique_items (bool | None):
            Indicates if all items in an array must be unique.
        maximum (float | None):
            The maximum value for numeric values.
        minimum (float | None):
            The minimum value for numeric values.
        nullable (bool | None):
            Indicates if the value can be null.
        pattern (str | None):
            A regular expression pattern for string values.
        xml (XML | None):
            Additional metadata for XML representation.
        items (None | "Schema" | "Reference"):
            The schema for items in an array.
        enum (list[str] | None):
            A list of allowed values for the schema.
        discriminator (Discriminator | None):
            The discriminator for polymorphism.
        all_of (list["Schema" | "Reference"] | None):
            A list of schemas that must all apply.
        any_of (list["Schema" | "Reference"] | None):
            A list of schemas where at least one must apply.
        one_of (list["Schema" | "Reference"] | None):
            A list of schemas where exactly one must apply.
        not_ (list["Schema" | "Reference"] | None):
            A schema that must not apply.
    """

    type: None | str | ValueType | list[None | str | ValueType] = None
    format: None | str | ValueFormat = None
    required: list[str] | None = None
    properties: dict[str, "Schema | Reference"] | None = None
    additional_properties: "None | bool | Schema | Reference" = None
    default: Any | None = None
    deprecated: bool | None = None
    example: Any | None = None
    external_docs: ExternalDocs | None = None
    ref: str | None = None
    title: str | None = None
    description: str | None = None
    content_encoding: str | None = None
    content_media_type: str | None = None
    pattern: str | None = None
    max_length: float | None = None
    min_length: float | None = None
    max_items: int | None = None
    min_items: int | None = None
    unique_items: bool | None = None
    maximum: float | None = None
    minimum: float | None = None
    nullable: bool | None = None
    xml: XML | None = None
    items: "None | Schema | Reference" = None
    enum: list[str] | None = None
    discriminator: Discriminator | None = None
    all_of: list["Schema | Reference"] | None = None
    any_of: list["Schema | Reference"] | None = None
    one_of: list["Schema | Reference"] | None = None
    not_: list["Schema | Reference"] | None = None


@dataclass
class Header(OpenAPIElement):
    """
    Represents a header object in OpenAPI.

    Attributes:
        description (str | None): A description of the header.
        schema (None | Schema | "Reference"): The schema defining the type used for the header.
    """

    description: str | None = None
    schema: "None | Schema | Reference" = None


@dataclass
class Example(OpenAPIElement):
    """
    Represents an example of a media type in OpenAPI.

    Attributes:
        summary (str | None): Short summary of the example.
        description (str | None): Detailed description of the example.
        value (Any | None): The embedded literal example. This field and external_value are mutually exclusive.
        external_value (str | None): A URL that points to the literal example. This field and value are mutually exclusive.
    """

    summary: str | None = None
    description: str | None = None
    value: Any | None = None
    external_value: str | None = None


@dataclass
class Reference(OpenAPIElement):
    """
    Represents a reference to another component in the OpenAPI specification.

    Attributes:
        ref (str): A reference string pointing to a component in the specification,
                  following the JSON Reference format.
        summary (str | None): A short summary which by default should override that of the
                                referenced component.
        description (str | None): A description which by default should override that of the
                                    referenced component.
    """

    ref: str
    summary: str | None = None
    description: str | None = None

    def to_obj(self) -> dict[str, str]:
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
        content_type (str | None): The Content-Type for encoding specific parts of the request body.
        headers (dict[str, Header | Reference] | None): A map of headers that are sent with the encoding defined by content_type.
        style (str | None): Describes how the parameter value will be serialized.
        explode (bool | None): When style is form, the default value is true, otherwise the default value is false.
        allow_reserved (bool | None): Determines whether the parameter value should allow reserved characters.
    """

    content_type: str | None = None
    headers: dict[str, Header | Reference] | None = None
    style: str | None = None
    explode: bool | None = None
    allow_reserved: bool | None = None


@dataclass
class Link(OpenAPIElement):
    """
    Represents a Link object in OpenAPI which describes a possible design-time link for a response.

    Attributes:
        operation_ref (str | None): A relative or absolute URI reference to an OAS operation.
        operation_id (str | None): The name of an existing, resolvable OAS operation.
        parameters (dict[str, Any] | None): A map representing parameters to pass to the linked operation.
        request_body (Any | None): A literal value or expression to use as a request body when calling the target operation.
        description (str | None): A description of the link.
        server (Server | None): A server object to be used by the target operation.
    """

    operation_ref: str | None = None
    operation_id: str | None = None
    parameters: dict[str, Any] | None = None
    request_body: Any | None = None
    description: str | None = None
    server: Server | None = None


@dataclass
class MediaType(OpenAPIElement):
    """
    Represents a media type in OpenAPI which provides schema and examples for a particular media type.

    Attributes:
        schema (None | Schema | Reference): The schema defining the content of the request, response, or parameter.
        examples (dict[str, Example | Reference] | None): Examples of the media type with their values.
        encoding (dict[str, Encoding] | None): A map between property names and their encoding information.
    """

    schema: None | Schema | Reference = None
    examples: dict[str, Example | Reference] | None = None
    encoding: dict[str, Encoding] | None = None


@dataclass
class Response(OpenAPIElement):
    """
    Represents a response in an OpenAPI operation.

    Attributes:
        description (str | None): A description of the response.
        headers (dict[str, Header | Reference] | None): A map of headers to be sent with the response.
        content (dict[str, MediaType | Reference] | None): A map containing descriptions of potential response payloads.
        links (dict[str, Link | Reference] | None): A map of operations that can be called from the response.
    """

    description: str | None = None
    headers: dict[str, Header | Reference] | None = None
    content: dict[str, MediaType | Reference] | None = None
    links: dict[str, Link | Reference] | None = None


@dataclass
class Parameter(OpenAPIElement):
    """
    Represents a parameter in an OpenAPI operation.

    Attributes:
        name (str): The name of the parameter.
        in_ (ParameterLocation): The location of the parameter (query, header, path, cookie).
        schema (None | Schema | Reference): The schema defining the type used for the parameter.
        content (dict[str, MediaType] | None): A map containing the representations for the parameter.
        description (str | None): A brief description of the parameter.
        required (bool | None): Determines whether this parameter is mandatory.
        deprecated (bool | None): Specifies that a parameter is deprecated.
        allow_empty_value (bool | None): Sets the ability to pass empty-valued parameters.
        example (Any | None): Example of the parameter's potential value.
        examples (dict[str, Example | Reference] | None): Examples of the parameter's potential value.
    """

    name: str
    in_: ParameterLocation
    schema: None | Schema | Reference = None
    content: dict[str, MediaType] | None = None
    description: str | None = None
    required: bool | None = None
    deprecated: bool | None = None
    allow_empty_value: bool | None = None
    example: Any | None = None
    examples: dict[str, Example | Reference] | None = None


@dataclass
class RequestBody(OpenAPIElement):
    """
    Represents a request body in an OpenAPI operation.

    Attributes:
        content (dict[str, MediaType]): A map containing descriptions of potential request payloads.
        description (str | None): A brief description of the request body.
        required (bool | None): Determines whether the request body is required in the API call.
    """

    content: dict[str, MediaType]
    description: str | None = None
    required: bool | None = None


@dataclass
class SecurityRequirement(OpenAPIElement):
    """
    Represents a security requirement in OpenAPI.

    Attributes:
        name (str): The name of the security scheme to use.
        value (list[str]): List of scope names required for the execution. Empty list means no scopes.
    """

    name: str
    value: list[str]

    def to_obj(self):
        return {self.name: self.value}


@dataclass
class Operation(OpenAPIElement):
    """
    Represents an operation in an OpenAPI path.

    Attributes:
        responses (dict[str, Response]): The responses available for this operation.
        tags (list[str] | None): Tags for API documentation control.
        summary (str | None): A short summary of what the operation does.
        description (str | None): A detailed explanation of the operation behavior.
        external_docs (ExternalDocs | None): Additional external documentation.
        operation_id (str | None): Unique string identifying the operation.
        parameters (list[Parameter | Reference] | None): Parameters that are applicable for this operation.
        request_body (RequestBody | Reference | None): The request body applicable for this operation.
        callbacks (dict[str, "Callback" | Reference] | None): Callbacks that may be initiated by the API provider.
        deprecated (bool | None): Declares this operation to be deprecated.
        security (list[SecurityRequirement] | None): Security requirements for this operation.
        servers (list[Server] | None): Servers that provide this operation.
    """

    responses: dict[str, Response]
    tags: list[str] | None = None
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocs | None = None
    operation_id: str | None = None
    parameters: list[Parameter | Reference] | None = None
    request_body: None | RequestBody | Reference = None
    callbacks: dict[str, "Callback | Reference"] | None = None
    deprecated: bool | None = None
    security: list[SecurityRequirement] | None = None
    servers: list[Server] | None = None


@dataclass
class PathItem(OpenAPIElement):
    """
    Represents a path item in an OpenAPI document.

    A PathItem describes the operations available on a single path. It can be directly accessed from
    an OpenAPI object's paths map, where each path is mapped to its associated PathItem object.

    Attributes:
        summary (str | None): A short summary of what the path represents.
        ref (str | None): Reference to another PathItem definition.
        description (str | None): A detailed explanation of the path's behavior.
        get (Operation | None): The GET operation for this path.
        put (Operation | None): The PUT operation for this path.
        post (Operation | None): The POST operation for this path.
        delete (Operation | None): The DELETE operation for this path.
        options (Operation | None): The OPTIONS operation for this path.
        head (Operation | None): The HEAD operation for this path.
        patch (Operation | None): The PATCH operation for this path.
        trace (Operation | None): The TRACE operation for this path.
        servers (list[Server] | None): Servers overriding the global servers for this path.
        parameters (list[Parameter | Reference] | None): Parameters common to all operations on this path.
    """

    summary: str | None = None
    ref: str | None = None
    description: str | None = None
    get: Operation | None = None
    put: Operation | None = None
    post: Operation | None = None
    delete: Operation | None = None
    options: Operation | None = None
    head: Operation | None = None
    patch: Operation | None = None
    trace: Operation | None = None
    servers: list[Server] | None = None
    parameters: list[Parameter | Reference] | None = None


@dataclass
class Callback(OpenAPIElement):
    """
    Represents a callback in an OpenAPI document.

    A Callback is a map of runtime expressions to path item objects that define the
    operations that will be invoked when the callback is triggered by the API provider.

    Attributes:
        expression (str): The runtime expression that specifies when the callback should be
                          invoked, such as a URL pointing to a callback destination.
        path (PathItem | Reference): The path item object or reference that defines
                                          the operations available on the callback destination.
    """

    expression: str
    path: PathItem | Reference

    def to_obj(self) -> dict[str, Any]:
        return {self.expression: normalize_dict(self.path)}


@dataclass
class OAuthFlow(OpenAPIElement):
    """
    Represents an OAuth flow configuration in OpenAPI.

    This class defines the configuration details for an OAuth 2.0 flow type, including
    available scopes and the authorization and token URLs needed for the flow.

    Attributes:
        scopes (dict[str, str]): Map between scope names and their descriptions.
        authorization_url (str | None): The authorization URL to be used for the flow.
                                          Required for implicit and authorizationCode flows.
        token_url (str | None): The token URL to be used for the flow.
                                  Required for password, clientCredentials, and authorizationCode flows.
        refresh_url (str | None): The URL to be used for obtaining refresh tokens.
    """

    scopes: dict[str, str]
    authorization_url: str | None = None
    token_url: str | None = None
    refresh_url: str | None = None


@dataclass
class OAuthFlows(OpenAPIElement):
    """
    Represents the available OAuth flows in an OpenAPI security scheme.

    This class contains configuration details for different OAuth 2.0 flows that can be used
    for authorization. Each flow type has its own configuration requirements.

    Attributes:
        implicit (OAuthFlow | None): Configuration for the OAuth Implicit flow.
        password (OAuthFlow | None): Configuration for the OAuth Resource Owner Password Credentials flow.
        client_credentials (OAuthFlow | None): Configuration for the OAuth Client Credentials flow.
        authorization_code (OAuthFlow | None): Configuration for the OAuth Authorization Code flow.
    """

    implicit: OAuthFlow | None = None
    password: OAuthFlow | None = None
    client_credentials: OAuthFlow | None = None
    authorization_code: OAuthFlow | None = None


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
        description (str | None): A description of the security scheme.
        bearer_format (str | None): A hint to the client to identify how the bearer token is formatted.
                                      For example, "JWT" for JSON Web Tokens.
    """

    scheme: str
    type: SecuritySchemeType = SecuritySchemeType.HTTP
    description: str | None = None
    bearer_format: str | None = None


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
        description (str | None): A description of the security scheme.
    """

    name: str
    in_: ParameterLocation
    type: SecuritySchemeType = SecuritySchemeType.APIKEY
    description: str | None = None


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
    description: str | None = None


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
        description (str | None): A description of the security scheme.
    """

    open_id_connect_url: str
    type: SecuritySchemeType = SecuritySchemeType.OPENIDCONNECT
    description: str | None = None


@dataclass
class MutualTLSSecurity(SecurityScheme):
    """
    Represents a Mutual TLS security scheme in OpenAPI.

    This class defines how mutual TLS (Transport Layer Security) can be used for authentication
    where both the client and server authenticate each other using X.509 certificates.

    Attributes:
        type (SecuritySchemeType): The type of the security scheme, always MUTUALTLS for this class.
        description (str | None): A description of the security scheme.
    """

    type: SecuritySchemeType = SecuritySchemeType.MUTUALTLS
    description: str | None = None


@dataclass
class Components(OpenAPIElement):
    """
    Represents the reusable components of an OpenAPI document.

    Attributes:
        schemas (dict[str, Schema | Reference] | None):
            A dictionary of reusable Schema Objects or references to them.
        responses (dict[str, Response | Reference] | None):
            A dictionary of reusable Response Objects or references to them.
        parameters (dict[str, Parameter | Reference] | None):
            A dictionary of reusable Parameter Objects or references to them.
        examples (dict[str, Example | Reference] | None):
            A dictionary of reusable Example Objects or references to them.
        request_bodies (dict[str, RequestBody | Reference] | None):
            A dictionary of reusable RequestBody Objects or references to them.
        headers (dict[str, Header | Reference] | None):
            A dictionary of reusable Header Objects or references to them.
        security_schemes (dict[str, SecurityScheme | Reference] | None):
            A dictionary of reusable SecurityScheme Objects or references to them.
        links (dict[str, Link | Reference] | None):
            A dictionary of reusable Link Objects or references to them.
        callbacks (dict[str, Callback | Reference] | None):
            A dictionary of reusable Callback Objects or references to them.
        path_items (dict[str, PathItem | Reference] | None):
            A dictionary of reusable PathItem Objects or references to them.
    """

    schemas: dict[str, Schema | Reference] | None = None
    responses: dict[str, Response | Reference] | None = None
    parameters: dict[str, Parameter | Reference] | None = None
    examples: dict[str, Example | Reference] | None = None
    request_bodies: dict[str, RequestBody | Reference] | None = None
    headers: dict[str, Header | Reference] | None = None
    security_schemes: dict[str, SecurityScheme | Reference] | None = None
    links: dict[str, Link | Reference] | None = None
    callbacks: dict[str, Callback | Reference] | None = None
    path_items: dict[str, PathItem | Reference] | None = None


@dataclass
class Tag(OpenAPIElement):
    """
    Represents a tag for API documentation control.

    Tags are used to group operations in the OpenAPI documentation, making the API
    documentation more organized and easier to navigate.

    Attributes:
        name (str): The name of the tag.
        description (str | None): A short description of the tag.
        external_docs (ExternalDocs | None): Additional external documentation for this tag.
    """

    name: str
    description: str | None = None
    external_docs: ExternalDocs | None = None


@dataclass
class Security(OpenAPIElement):
    """
    Represents security requirements in an OpenAPI document.

    This class defines the security mechanisms required by the API. It allows for specifying
    alternative security requirement objects that can be used.

    Attributes:
        requirements (list[SecurityRequirement]): List of security requirement objects that
                                                  define the security mechanisms for the API.
        optional (bool): When set to True, indicates that security is optional by adding an
                         empty security requirement at the beginning of the list.
    """

    requirements: list[SecurityRequirement]
    optional: bool = False

    def to_obj(self) -> list[dict[str, Any]]:
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
        info (Info | None): Metadata about the API.
        json_schema_dialect (str): The default value for the $schema keyword within Schema Objects contained
                                  within this OAS document.
        paths (dict[str, PathItem] | None): The available paths and operations for the API.
        servers (list[Server] | None): An array of Server Objects that provide connectivity information
                                        to a target server.
        components (Components | None): Holds various reusable schemas for the specification.
        tags (list[Tag] | None): A list of tags used by the specification with additional metadata.
        security (Security | None): A declaration of which security mechanisms can be used across the API.
        external_docs (ExternalDocs | None): Additional external documentation.
        webhooks (dict[str, PathItem | Reference] | None): Webhook definitions that MAY be called by the API provider.
    """

    openapi: str = "3.1.0"
    info: Info | None = None
    json_schema_dialect: str = "https://json-schema.org/draft/2020-12/schema"
    paths: dict[str, PathItem] | None = None
    servers: list[Server] | None = None
    components: Components | None = None
    tags: list[Tag] | None = None
    security: Security | None = None
    external_docs: ExternalDocs | None = None
    webhooks: dict[str, PathItem | Reference] | None = None
