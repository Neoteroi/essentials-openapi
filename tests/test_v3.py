from abc import abstractmethod
from dataclasses import dataclass
from textwrap import dedent
from tests.common import debug_result
from typing import Any, Type

import pytest
from openapidocs.common import Format, Serializer
from openapidocs.v3 import (
    APIKeySecurity,
    Callback,
    Components,
    Contact,
    Example,
    HTTPSecurity,
    Info,
    License,
    MediaType,
    OAuth2Security,
    OAuthFlow,
    OAuthFlows,
    OpenAPI,
    ValueType,
    OpenIdConnectSecurity,
    Operation,
    Parameter,
    ParameterLocation,
    PathItem,
    Reference,
    RequestBody,
    Response,
    Schema,
    Security,
    SecurityRequirement,
    Server,
    ServerVariable,
)


@dataclass
class ExampleOne:
    snake_case: str
    ner_label: str


class TestItem:
    @abstractmethod
    def get_instance(self) -> Any:
        ...

    def expected_yaml(self) -> str:
        return dedent(self.yaml()).strip()

    def expected_json(self) -> str:
        return dedent(self.json()).strip()

    @abstractmethod
    def json(self) -> str:
        ...

    @abstractmethod
    def yaml(self) -> str:
        ...


class ParameterExample1(TestItem):
    def get_instance(self) -> Parameter:
        return Parameter("search", ParameterLocation.QUERY)

    def yaml(self) -> str:
        return """
        name: search
        in: query
        """

    def json(self) -> str:
        return """
        {
            "name": "search",
            "in": "query"
        }
        """


class OpenAPIExample1(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Cats API", version="1.0.0"),
            paths={
                "/": PathItem("summary"),
                "/api/v1/cats": PathItem(
                    "",
                    get=Operation(
                        responses={"200": Response("Gets a list of cats")},
                        parameters=[
                            Parameter(
                                "page",
                                ParameterLocation.QUERY,
                                schema=Schema(type="integer"),
                            ),
                            Parameter(
                                "size",
                                ParameterLocation.QUERY,
                                schema=Schema(type="integer"),
                            ),
                            Parameter(
                                "search",
                                ParameterLocation.QUERY,
                                schema=Schema(type="string"),
                            ),
                        ],
                    ),
                ),
            },
            servers=[
                Server("https://dev.foo.com", "Development server"),
                Server("https://test.foo.com", "Test server"),
                Server("https://foo.com", "Production server"),
            ],
        )

    def yaml(self) -> str:
        return """
        openapi: 3.0.3
        info:
            title: Cats API
            version: 1.0.0
        paths:
            /:
                summary: summary
            /api/v1/cats:
                summary: ''
                get:
                    responses:
                        '200':
                            description: Gets a list of cats
                    parameters:
                    -   name: page
                        in: query
                        schema:
                            type: integer
                    -   name: size
                        in: query
                        schema:
                            type: integer
                    -   name: search
                        in: query
                        schema:
                            type: string
        servers:
        -   url: https://dev.foo.com
            description: Development server
        -   url: https://test.foo.com
            description: Test server
        -   url: https://foo.com
            description: Production server
        """

    def json(self) -> str:
        return """
        {
            "openapi": "3.0.3",
            "info": {
                "title": "Cats API",
                "version": "1.0.0"
            },
            "paths": {
                "/": {
                    "summary": "summary"
                },
                "/api/v1/cats": {
                    "summary": "",
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Gets a list of cats"
                            }
                        },
                        "parameters": [
                            {
                                "name": "page",
                                "in": "query",
                                "schema": {
                                    "type": "integer"
                                }
                            },
                            {
                                "name": "size",
                                "in": "query",
                                "schema": {
                                    "type": "integer"
                                }
                            },
                            {
                                "name": "search",
                                "in": "query",
                                "schema": {
                                    "type": "string"
                                }
                            }
                        ]
                    }
                }
            },
            "servers": [
                {
                    "url": "https://dev.foo.com",
                    "description": "Development server"
                },
                {
                    "url": "https://test.foo.com",
                    "description": "Test server"
                },
                {
                    "url": "https://foo.com",
                    "description": "Production server"
                }
            ]
        }
        """


class OpenAPIExample2(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Cats API", version="1.0.0"),
            paths={
                "/": PathItem("summary"),
                "/api/v1/cats": PathItem(
                    "",
                    get=Operation(
                        responses={"200": Response("Gets a list of cats")},
                        parameters=[
                            Parameter(
                                "page",
                                ParameterLocation.QUERY,
                                schema=Schema(type="integer"),
                            ),
                            Parameter(
                                "size",
                                ParameterLocation.QUERY,
                                schema=Schema(type="integer"),
                            ),
                            Parameter(
                                "search",
                                ParameterLocation.QUERY,
                                schema=Schema(type="string"),
                            ),
                        ],
                    ),
                ),
            },
            servers=[
                Server("https://dev.foo.com", "Development server"),
                Server("https://test.foo.com", "Test server"),
                Server("https://foo.com", "Production server"),
            ],
            components=Components(
                security_schemes={
                    "BasicAuth": HTTPSecurity(scheme="basic"),
                    "BearerAuth": HTTPSecurity(scheme="bearer"),
                    "ApiKeyAuth": APIKeySecurity(
                        in_=ParameterLocation.HEADER,
                        name="X-API-Key",
                    ),
                    "OpenID": OpenIdConnectSecurity(
                        open_id_connect_url="https://example.com/.well-known/openid-configuration"
                    ),
                    "OAuth2": OAuth2Security(
                        flows=OAuthFlows(
                            authorization_code=OAuthFlow(
                                {
                                    "read": "Grants read access",
                                    "write": "Grants write access",
                                    "admin": "Grants access to admin operations",
                                },
                                authorization_url="https://example.com/oauth/authorize",
                                token_url="https://example.com/oauth/token",
                            )
                        )
                    ),
                }
            ),
            security=Security(
                [
                    SecurityRequirement("ApiKeyAuth", []),
                    SecurityRequirement("OAuth2", ["read", "write"]),
                ],
                optional=True,
            ),
        )

    def yaml(self) -> str:
        return """
        openapi: 3.0.3
        info:
            title: Cats API
            version: 1.0.0
        paths:
            /:
                summary: summary
            /api/v1/cats:
                summary: ''
                get:
                    responses:
                        '200':
                            description: Gets a list of cats
                    parameters:
                    -   name: page
                        in: query
                        schema:
                            type: integer
                    -   name: size
                        in: query
                        schema:
                            type: integer
                    -   name: search
                        in: query
                        schema:
                            type: string
        servers:
        -   url: https://dev.foo.com
            description: Development server
        -   url: https://test.foo.com
            description: Test server
        -   url: https://foo.com
            description: Production server
        components:
            securitySchemes:
                BasicAuth:
                    scheme: basic
                    type: http
                BearerAuth:
                    scheme: bearer
                    type: http
                ApiKeyAuth:
                    name: X-API-Key
                    in: header
                    type: apiKey
                OpenID:
                    openIdConnectUrl: https://example.com/.well-known/openid-configuration
                    type: openIdConnect
                OAuth2:
                    flows:
                        authorizationCode:
                            scopes:
                                read: Grants read access
                                write: Grants write access
                                admin: Grants access to admin operations
                            authorizationUrl: https://example.com/oauth/authorize
                            tokenUrl: https://example.com/oauth/token
                    type: oauth2
        security:
        - {}
        -   ApiKeyAuth: []
        -   OAuth2:
            - read
            - write
        """

    def json(self) -> str:
        return """
        {
            "openapi": "3.0.3",
            "info": {
                "title": "Cats API",
                "version": "1.0.0"
            },
            "paths": {
                "/": {
                    "summary": "summary"
                },
                "/api/v1/cats": {
                    "summary": "",
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Gets a list of cats"
                            }
                        },
                        "parameters": [
                            {
                                "name": "page",
                                "in": "query",
                                "schema": {
                                    "type": "integer"
                                }
                            },
                            {
                                "name": "size",
                                "in": "query",
                                "schema": {
                                    "type": "integer"
                                }
                            },
                            {
                                "name": "search",
                                "in": "query",
                                "schema": {
                                    "type": "string"
                                }
                            }
                        ]
                    }
                }
            },
            "servers": [
                {
                    "url": "https://dev.foo.com",
                    "description": "Development server"
                },
                {
                    "url": "https://test.foo.com",
                    "description": "Test server"
                },
                {
                    "url": "https://foo.com",
                    "description": "Production server"
                }
            ],
            "components": {
                "securitySchemes": {
                    "BasicAuth": {
                        "scheme": "basic",
                        "type": "http"
                    },
                    "BearerAuth": {
                        "scheme": "bearer",
                        "type": "http"
                    },
                    "ApiKeyAuth": {
                        "name": "X-API-Key",
                        "in": "header",
                        "type": "apiKey"
                    },
                    "OpenID": {
                        "openIdConnectUrl": "https://example.com/.well-known/openid-configuration",
                        "type": "openIdConnect"
                    },
                    "OAuth2": {
                        "flows": {
                            "authorizationCode": {
                                "scopes": {
                                    "read": "Grants read access",
                                    "write": "Grants write access",
                                    "admin": "Grants access to admin operations"
                                },
                                "authorizationUrl": "https://example.com/oauth/authorize",
                                "tokenUrl": "https://example.com/oauth/token"
                            }
                        },
                        "type": "oauth2"
                    }
                }
            },
            "security": [
                {},
                {
                    "ApiKeyAuth": []
                },
                {
                    "OAuth2": [
                        "read",
                        "write"
                    ]
                }
            ]
        }
        """


class OpenAPIExample3(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Weather API", version="0.0.0-alpha"),
            paths={
                "/weather": PathItem(
                    summary="Call current weather data for one location",
                    description="""Access current weather data for any location on Earth.""",
                    get=Operation(
                        tags=["Current Weather Data"],
                        operation_id="CurrentWeatherData",
                        parameters=[
                            Reference("#/components/parameters/q"),
                            Reference("#/components/parameters/id"),
                            Reference("#/components/parameters/lat"),
                            Reference("#/components/parameters/lon"),
                        ],
                        responses={
                            "200": Response(
                                "Successful response",
                                content={
                                    "application/json": MediaType(
                                        schema=Schema(
                                            ValueType.OBJECT,
                                            title="sample",
                                            properties={
                                                "placeholder": Schema(
                                                    ValueType.STRING,
                                                    "Placeholder description",
                                                )
                                            },
                                        )
                                    )
                                },
                            ),
                            "404": Response(
                                "Not found response",
                                content={
                                    "text/plain": MediaType(
                                        schema=Schema(
                                            ValueType.STRING,
                                            title="Weather not found",
                                            example="Not found",
                                        )
                                    )
                                },
                            ),
                        },
                    ),
                )
            },
            components=Components(
                parameters={
                    "q": Parameter(
                        "q",
                        in_=ParameterLocation.QUERY,
                        description="Example",
                        schema=Schema(type=ValueType.STRING),
                    ),
                    "id": Parameter(
                        "id",
                        in_=ParameterLocation.QUERY,
                        description="Example",
                        schema=Schema(type=ValueType.STRING),
                    ),
                    "lat": Parameter(
                        "lat",
                        in_=ParameterLocation.QUERY,
                        description="Example",
                        schema=Schema(type=ValueType.STRING),
                    ),
                    "lon": Parameter(
                        "lon",
                        in_=ParameterLocation.QUERY,
                        description="Example",
                        schema=Schema(type=ValueType.STRING),
                    ),
                }
            ),
        )

    def yaml(self) -> str:
        return """
        openapi: 3.0.3
        info:
            title: Weather API
            version: 0.0.0-alpha
        paths:
            /weather:
                summary: Call current weather data for one location
                description: Access current weather data for any location on Earth.
                get:
                    responses:
                        '200':
                            description: Successful response
                            content:
                                application/json:
                                    schema:
                                        type: object
                                        properties:
                                            placeholder:
                                                type: string
                                                format: Placeholder description
                                        title: sample
                        '404':
                            description: Not found response
                            content:
                                text/plain:
                                    schema:
                                        type: string
                                        example: Not found
                                        title: Weather not found
                    tags:
                    - Current Weather Data
                    operationId: CurrentWeatherData
                    parameters:
                    -   $ref: '#/components/parameters/q'
                    -   $ref: '#/components/parameters/id'
                    -   $ref: '#/components/parameters/lat'
                    -   $ref: '#/components/parameters/lon'
        components:
            parameters:
                q:
                    name: q
                    in: query
                    schema:
                        type: string
                    description: Example
                id:
                    name: id
                    in: query
                    schema:
                        type: string
                    description: Example
                lat:
                    name: lat
                    in: query
                    schema:
                        type: string
                    description: Example
                lon:
                    name: lon
                    in: query
                    schema:
                        type: string
                    description: Example
        """

    def json(self) -> str:
        return """
        {
            "openapi": "3.0.3",
            "info": {
                "title": "Weather API",
                "version": "0.0.0-alpha"
            },
            "paths": {
                "/weather": {
                    "summary": "Call current weather data for one location",
                    "description": "Access current weather data for any location on Earth.",
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "placeholder": {
                                                    "type": "string",
                                                    "format": "Placeholder description"
                                                }
                                            },
                                            "title": "sample"
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Not found response",
                                "content": {
                                    "text/plain": {
                                        "schema": {
                                            "type": "string",
                                            "example": "Not found",
                                            "title": "Weather not found"
                                        }
                                    }
                                }
                            }
                        },
                        "tags": [
                            "Current Weather Data"
                        ],
                        "operationId": "CurrentWeatherData",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/q"
                            },
                            {
                                "$ref": "#/components/parameters/id"
                            },
                            {
                                "$ref": "#/components/parameters/lat"
                            },
                            {
                                "$ref": "#/components/parameters/lon"
                            }
                        ]
                    }
                }
            },
            "components": {
                "parameters": {
                    "q": {
                        "name": "q",
                        "in": "query",
                        "schema": {
                            "type": "string"
                        },
                        "description": "Example"
                    },
                    "id": {
                        "name": "id",
                        "in": "query",
                        "schema": {
                            "type": "string"
                        },
                        "description": "Example"
                    },
                    "lat": {
                        "name": "lat",
                        "in": "query",
                        "schema": {
                            "type": "string"
                        },
                        "description": "Example"
                    },
                    "lon": {
                        "name": "lon",
                        "in": "query",
                        "schema": {
                            "type": "string"
                        },
                        "description": "Example"
                    }
                }
            }
        }
        """


class OpenAPIExample4(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Example API", version="0.0.0-alpha"),
            paths={
                "/": PathItem(
                    summary="Test the example snake_case properness",
                    description="Lorem ipsum dolor sit amet",
                    get=Operation(
                        tags=["Example"],
                        operation_id="example",
                        parameters=[],
                        responses={
                            "200": Response(
                                "Successful response",
                                content={
                                    "application/json": MediaType(
                                        schema=Schema(
                                            ValueType.OBJECT,
                                            title="sample",
                                            properties={
                                                "snake_case": Schema(
                                                    ValueType.STRING,
                                                    "Placeholder description",
                                                ),
                                                "ner_label": Schema(
                                                    ValueType.STRING,
                                                    "Placeholder description",
                                                ),
                                            },
                                            example=ExampleOne(
                                                snake_case="Foo",
                                                ner_label="Lorem Ipsum",
                                            ),
                                        )
                                    )
                                },
                            ),
                        },
                    ),
                )
            },
        )

    def yaml(self) -> str:
        return """
openapi: 3.0.3
info:
    title: Example API
    version: 0.0.0-alpha
paths:
    /:
        summary: Test the example snake_case properness
        description: Lorem ipsum dolor sit amet
        get:
            responses:
                '200':
                    description: Successful response
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    snake_case:
                                        type: string
                                        format: Placeholder description
                                    ner_label:
                                        type: string
                                        format: Placeholder description
                                example:
                                    snake_case: Foo
                                    ner_label: Lorem Ipsum
                                title: sample
            tags:
            - Example
            operationId: example
            parameters: []
    """

    def json(self) -> str:
        return """
{
    "openapi": "3.0.3",
    "info": {
        "title": "Example API",
        "version": "0.0.0-alpha"
    },
    "paths": {
        "/": {
            "summary": "Test the example snake_case properness",
            "description": "Lorem ipsum dolor sit amet",
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "snake_case": {
                                            "type": "string",
                                            "format": "Placeholder description"
                                        },
                                        "ner_label": {
                                            "type": "string",
                                            "format": "Placeholder description"
                                        }
                                    },
                                    "example": {
                                        "snake_case": "Foo",
                                        "ner_label": "Lorem Ipsum"
                                    },
                                    "title": "sample"
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Example"
                ],
                "operationId": "example",
                "parameters": []
            }
        }
    }
}
    """


class OpenAPIExample5(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Example API", version="0.0.0-alpha"),
            paths={
                "/": PathItem(
                    summary="Test the example snake_case properness",
                    description="Lorem ipsum dolor sit amet",
                    get=Operation(
                        tags=["Example"],
                        operation_id="example",
                        parameters=[],
                        responses={
                            "200": Response(
                                "Successful response",
                                content={
                                    "application/json": MediaType(
                                        schema=Schema(
                                            ValueType.OBJECT,
                                            title="sample",
                                            properties={
                                                "snake_case": Schema(
                                                    ValueType.STRING,
                                                    "Placeholder description",
                                                ),
                                                "ner_label": Schema(
                                                    ValueType.STRING,
                                                    "Placeholder description",
                                                ),
                                            },
                                        ),
                                        examples={
                                            "one": Example(
                                                summary="First example",
                                                value=ExampleOne(
                                                    snake_case="ABC",
                                                    ner_label="Lorem Ipsum 1",
                                                ),
                                            ),
                                            "two": Example(
                                                summary="Second example",
                                                value=ExampleOne(
                                                    snake_case="DEF",
                                                    ner_label="Lorem Ipsum 2",
                                                ),
                                            ),
                                        },
                                    )
                                },
                            ),
                        },
                    ),
                )
            },
        )

    def yaml(self) -> str:
        return """
openapi: 3.0.3
info:
    title: Example API
    version: 0.0.0-alpha
paths:
    /:
        summary: Test the example snake_case properness
        description: Lorem ipsum dolor sit amet
        get:
            responses:
                '200':
                    description: Successful response
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    snake_case:
                                        type: string
                                        format: Placeholder description
                                    ner_label:
                                        type: string
                                        format: Placeholder description
                                title: sample
                            examples:
                                one:
                                    summary: First example
                                    value:
                                        snake_case: ABC
                                        ner_label: Lorem Ipsum 1
                                two:
                                    summary: Second example
                                    value:
                                        snake_case: DEF
                                        ner_label: Lorem Ipsum 2
            tags:
            - Example
            operationId: example
            parameters: []
    """

    def json(self) -> str:
        return """
{
    "openapi": "3.0.3",
    "info": {
        "title": "Example API",
        "version": "0.0.0-alpha"
    },
    "paths": {
        "/": {
            "summary": "Test the example snake_case properness",
            "description": "Lorem ipsum dolor sit amet",
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "snake_case": {
                                            "type": "string",
                                            "format": "Placeholder description"
                                        },
                                        "ner_label": {
                                            "type": "string",
                                            "format": "Placeholder description"
                                        }
                                    },
                                    "title": "sample"
                                },
                                "examples": {
                                    "one": {
                                        "summary": "First example",
                                        "value": {
                                            "snake_case": "ABC",
                                            "ner_label": "Lorem Ipsum 1"
                                        }
                                    },
                                    "two": {
                                        "summary": "Second example",
                                        "value": {
                                            "snake_case": "DEF",
                                            "ner_label": "Lorem Ipsum 2"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "tags": [
                    "Example"
                ],
                "operationId": "example",
                "parameters": []
            }
        }
    }
}
    """


class SchemaExample1(TestItem):
    def get_instance(self) -> Any:
        return Schema(
            type="object",
            required=["name"],
            properties={
                "name": Schema(type="string"),
                "address": Schema(ref="#/components/schemas/Address"),
                "age": Schema(type="integer", format="int32", minimum=0),
            },
        )

    def yaml(self) -> str:
        return """
        type: object
        required:
        - name
        properties:
            name:
                type: string
            address:
                $ref: '#/components/schemas/Address'
            age:
                type: integer
                format: int32
                minimum: 0
        """

    def json(self) -> str:
        return """
        {
            "type": "object",
            "required": [
                "name"
            ],
            "properties": {
                "name": {
                    "type": "string"
                },
                "address": {
                    "$ref": "#/components/schemas/Address"
                },
                "age": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 0
                }
            }
        }
        """


class ServerExample1(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            servers=[
                Server(
                    url="https://{username}.gigantic-server.com:{port}/{basePath}",
                    description="The production API server",
                    variables={
                        "username": ServerVariable(
                            default="demo",
                            description="this value is assigned by the service "
                            + " provider, in this example `gigantic-server.com`",
                        ),
                        "port": ServerVariable(
                            enum=["8443", "443"],
                            default="8443",
                        ),
                        "basePath": ServerVariable(
                            default="v2",
                        ),
                    },
                )
            ]
        )

    def yaml(self) -> str:
        return """
        openapi: 3.0.3
        servers:
        -   url: https://{username}.gigantic-server.com:{port}/{basePath}
            description: The production API server
            variables:
                username:
                    default: demo
                    description: this value is assigned by the service  provider, in this
                        example `gigantic-server.com`
                port:
                    default: '8443'
                    enum:
                    - '8443'
                    - '443'
                basePath:
                    default: v2
        """

    def json(self) -> str:
        return """
        {
            "openapi": "3.0.3",
            "servers": [
                {
                    "url": "https://{username}.gigantic-server.com:{port}/{basePath}",
                    "description": "The production API server",
                    "variables": {
                        "username": {
                            "default": "demo",
                            "description": "this value is assigned by the service  provider, in this example `gigantic-server.com`"
                        },
                        "port": {
                            "default": "8443",
                            "enum": [
                                "8443",
                                "443"
                            ]
                        },
                        "basePath": {
                            "default": "v2"
                        }
                    }
                }
            ]
        }
        """


class InfoExample1(TestItem):
    def get_instance(self) -> Any:
        return Info(
            title="Sample Pet Store App",
            description="This is a sample server for a pet store.",
            terms_of_service="http://example.com/terms/",
            contact=Contact(
                name="API Support",
                url="http://www.example.com/support",
                email="support@example.com",
            ),
            license=License(
                name="Apache 2.0",
                url="https://www.apache.org/licenses/LICENSE-2.0.html",
            ),
            version="1.0.1",
        )

    def yaml(self) -> str:
        return """
        title: Sample Pet Store App
        version: 1.0.1
        description: This is a sample server for a pet store.
        termsOfService: http://example.com/terms/
        contact:
            name: API Support
            url: http://www.example.com/support
            email: support@example.com
        license:
            name: Apache 2.0
            url: https://www.apache.org/licenses/LICENSE-2.0.html
        """

    def json(self) -> str:
        return """
        {
            "title": "Sample Pet Store App",
            "version": "1.0.1",
            "description": "This is a sample server for a pet store.",
            "termsOfService": "http://example.com/terms/",
            "contact": {
                "name": "API Support",
                "url": "http://www.example.com/support",
                "email": "support@example.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        }
        """


class InfoExample2(TestItem):
    def get_instance(self) -> Any:
        return Info(
            title="Sample Pet Store App",
            description="This is a sample server for a pet store.",
            license=License(
                name="Apache 2.0",
                url="https://www.apache.org/licenses/LICENSE-2.0.html",
            ),
            version="1.0.1",
        )

    def yaml(self) -> str:
        return """
        title: Sample Pet Store App
        version: 1.0.1
        description: This is a sample server for a pet store.
        license:
            name: Apache 2.0
            url: https://www.apache.org/licenses/LICENSE-2.0.html
        """

    def json(self) -> str:
        return """
        {
            "title": "Sample Pet Store App",
            "version": "1.0.1",
            "description": "This is a sample server for a pet store.",
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        }
        """


class InfoExample3(TestItem):
    def get_instance(self) -> Any:
        return Info(
            title="ØØ Void",
            description="Great album.",
            version="1.0.1",
        )

    def yaml(self) -> str:
        return """
        title: ØØ Void
        version: 1.0.1
        description: Great album.
        """

    def json(self) -> str:
        return """
        {
            "title": "ØØ Void",
            "version": "1.0.1",
            "description": "Great album."
        }
        """


class ResponseExample1(TestItem):
    def get_instance(self) -> Any:
        return Response(
            description="A simple string response",
            content={"text/plain": MediaType(schema=Schema(type="string"))},
        )

    def yaml(self) -> str:
        return """
        description: A simple string response
        content:
            text/plain:
                schema:
                    type: string
        """

    def json(self) -> str:
        return """
        {
            "description": "A simple string response",
            "content": {
                "text/plain": {
                    "schema": {
                        "type": "string"
                    }
                }
            }
        }
        """


class RequestBodyExample1(TestItem):
    def get_instance(self) -> Any:
        return RequestBody(
            description="Some request body",
            content={
                "text/plain": MediaType(schema=Schema(type=ValueType.STRING)),
                "application/json": MediaType(
                    schema=Schema(
                        type=ValueType.OBJECT,
                        required=["id", "name", "foo"],
                        properties={
                            "id": Schema(type=ValueType.STRING),
                            "name": Schema(type=ValueType.STRING),
                            "foo": Schema(type=ValueType.BOOLEAN),
                        },
                    )
                ),
            },
        )

    def yaml(self) -> str:
        return """
        content:
            text/plain:
                schema:
                    type: string
            application/json:
                schema:
                    type: object
                    required:
                    - id
                    - name
                    - foo
                    properties:
                        id:
                            type: string
                        name:
                            type: string
                        foo:
                            type: boolean
        description: Some request body
        """

    def json(self) -> str:
        return """
        {
            "content": {
                "text/plain": {
                    "schema": {
                        "type": "string"
                    }
                },
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": [
                            "id",
                            "name",
                            "foo"
                        ],
                        "properties": {
                            "id": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "foo": {
                                "type": "boolean"
                            }
                        }
                    }
                }
            },
            "description": "Some request body"
        }
        """


class SecuritySchemeExample1(TestItem):
    def get_instance(self) -> Any:
        return OAuth2Security(
            flows=OAuthFlows(
                implicit=OAuthFlow(
                    authorization_url="https://example.com/api/oauth/dialog",
                    scopes={
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets",
                    },
                ),
                authorization_code=OAuthFlow(
                    authorization_url="https://example.com/api/oauth/dialog",
                    token_url="https://example.com/api/oauth/token",
                    scopes={
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets",
                    },
                ),
            ),
        )

    def yaml(self) -> str:
        return """
        flows:
            implicit:
                scopes:
                    write:pets: modify pets in your account
                    read:pets: read your pets
                authorizationUrl: https://example.com/api/oauth/dialog
            authorizationCode:
                scopes:
                    write:pets: modify pets in your account
                    read:pets: read your pets
                authorizationUrl: https://example.com/api/oauth/dialog
                tokenUrl: https://example.com/api/oauth/token
        type: oauth2
        """

    def json(self) -> str:
        return """
        {
            "flows": {
                "implicit": {
                    "scopes": {
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets"
                    },
                    "authorizationUrl": "https://example.com/api/oauth/dialog"
                },
                "authorizationCode": {
                    "scopes": {
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets"
                    },
                    "authorizationUrl": "https://example.com/api/oauth/dialog",
                    "tokenUrl": "https://example.com/api/oauth/token"
                }
            },
            "type": "oauth2"
        }
        """


class CallbackExample1(TestItem):
    def get_instance(self) -> Any:
        return Callback(
            expression="{$request.query.queryUrl}",
            path=PathItem(
                post=Operation(
                    request_body=RequestBody(
                        description="Callback payload",
                        content={
                            "application/json": MediaType(
                                Schema(ref="#/components/schemas/SomePayload")
                            )
                        },
                    ),
                    responses={
                        "200": Response(description="callback successfully processed")
                    },
                )
            ),
        )

    def yaml(self) -> str:
        return """
        '{$request.query.queryUrl}':
            post:
                responses:
                    '200':
                        description: callback successfully processed
                requestBody:
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/SomePayload'
                    description: Callback payload
        """

    def json(self) -> str:
        return """
        {
            "{$request.query.queryUrl}": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "callback successfully processed"
                        }
                    },
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/SomePayload"
                                }
                            }
                        },
                        "description": "Callback payload"
                    }
                }
            }
        }
        """


@pytest.fixture(scope="module")
def serializer() -> Serializer:
    return Serializer()


@pytest.mark.parametrize("example_type", TestItem.__subclasses__())
def test_yaml_serialization(
    example_type: Type[TestItem], serializer: Serializer
) -> None:
    example = example_type()
    expected_yaml = example.expected_yaml()
    instance = example.get_instance()
    result = serializer.to_yaml(instance)
    try:
        assert result.strip() == expected_yaml
    except AssertionError as ae:
        debug_result("v3", example, result, Format.YAML)
        raise ae


@pytest.mark.parametrize("example_type", TestItem.__subclasses__())
def test_json_serialization(
    example_type: Type[TestItem], serializer: Serializer
) -> None:
    example = example_type()
    expected_json = example.expected_json()
    instance = example.get_instance()
    result = serializer.to_json(instance)
    try:
        assert result.strip() == expected_json
    except AssertionError as ae:
        debug_result("v3", example, result, Format.JSON)
        raise ae


@pytest.mark.parametrize("example_type", TestItem.__subclasses__())
def test_equality(example_type: Type[TestItem]) -> None:
    example = example_type()
    one = example.get_instance()
    two = example.get_instance()
    assert one == two
