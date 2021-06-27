from abc import abstractmethod
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Type

import pytest

from openapidocs.common import Format, Serializer
from openapidocs.v2 import (
    APIKeyLocation,
    APIKeySecurity,
    CollectionFormat,
    Contact,
    ExternalDocs,
    Header,
    HeaderType,
    Info,
    Items,
    License,
    OAuth2Security,
    OAuthFlowType,
    OpenAPI,
    Operation,
    Parameter,
    ParameterLocation,
    PathItem,
    Reference,
    Response,
    Schema,
    SecurityRequirement,
    ValueFormat,
    ValueItemType,
    ValueType,
    get_ref,
)
from tests.common import debug_result


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


class ParameterExample2(TestItem):
    def get_instance(self) -> Parameter:
        return Parameter(
            "name",
            ParameterLocation.BODY,
            description="user to add to the system",
            required=True,
            schema=Schema(type=ValueType.ARRAY, items=Schema(type=ValueType.STRING)),
        )

    def yaml(self) -> str:
        return """
        name: name
        in: body
        schema:
            type: array
            items:
                type: string
        description: user to add to the system
        required: true
        """

    def json(self) -> str:
        return """
        {
            "name": "name",
            "in": "body",
            "schema": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "description": "user to add to the system",
            "required": true
        }
        """


class ParameterExample3(TestItem):
    def get_instance(self) -> Parameter:
        return Parameter(
            "name",
            ParameterLocation.BODY,
            description="user to add to the system",
            required=True,
            schema=Schema(
                type=ValueType.OBJECT,
                example=ExampleOne(snake_case="Lorem ipsum", ner_label="Foo"),
            ),
        )

    def yaml(self) -> str:
        return """
        name: name
        in: body
        schema:
            type: object
            example:
                snake_case: Lorem ipsum
                ner_label: Foo
        description: user to add to the system
        required: true
        """

    def json(self) -> str:
        return """
        {
            "name": "name",
            "in": "body",
            "schema": {
                "type": "object",
                "example": {
                    "snake_case": "Lorem ipsum",
                    "ner_label": "Foo"
                }
            },
            "description": "user to add to the system",
            "required": true
        }
        """


class OpenAPIExample1(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Cats API", version="1.0.0"),
            paths={
                "/": PathItem(
                    get=Operation(responses={"200": Response("Gets the homepage")}),
                ),
                "/api/v1/cats": PathItem(
                    get=Operation(
                        responses={"200": Response("Gets a list of cats")},
                        parameters=[
                            Parameter(
                                "page",
                                ParameterLocation.QUERY,
                                type=ValueType.INTEGER,
                            ),
                            Parameter(
                                "size",
                                ParameterLocation.QUERY,
                                type=ValueType.INTEGER,
                            ),
                            Parameter(
                                "search",
                                ParameterLocation.QUERY,
                                type=ValueType.STRING,
                            ),
                        ],
                    ),
                ),
            },
        )

    def yaml(self) -> str:
        return """
        swagger: '2.0'
        info:
            title: Cats API
            version: 1.0.0
        paths:
            /:
                get:
                    responses:
                        '200':
                            description: Gets the homepage
            /api/v1/cats:
                get:
                    responses:
                        '200':
                            description: Gets a list of cats
                    parameters:
                    -   name: page
                        in: query
                        type: integer
                    -   name: size
                        in: query
                        type: integer
                    -   name: search
                        in: query
                        type: string
        """

    def json(self) -> str:
        return """
        {
            "swagger": "2.0",
            "info": {
                "title": "Cats API",
                "version": "1.0.0"
            },
            "paths": {
                "/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Gets the homepage"
                            }
                        }
                    }
                },
                "/api/v1/cats": {
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
                                "type": "integer"
                            },
                            {
                                "name": "size",
                                "in": "query",
                                "type": "integer"
                            },
                            {
                                "name": "search",
                                "in": "query",
                                "type": "string"
                            }
                        ]
                    }
                }
            }
        }
        """


class OpenAPIExample2(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info("Cats API", version="1.0.0"),
            paths={
                "/api/v1/cats": PathItem(
                    get=Operation(
                        responses={"200": Response("Gets a list of cats")},
                        parameters=[
                            Parameter(
                                "page",
                                ParameterLocation.QUERY,
                                type=ValueType.INTEGER,
                            ),
                            Parameter(
                                "size",
                                ParameterLocation.QUERY,
                                type=ValueType.INTEGER,
                            ),
                            Parameter(
                                "search",
                                ParameterLocation.QUERY,
                                type=ValueType.STRING,
                            ),
                        ],
                    ),
                ),
            },
            security_definitions={
                "api_key": APIKeySecurity("api_key", in_=APIKeyLocation.HEADER),
                "petstore_auth": OAuth2Security(
                    authorization_url="http://swagger.io/api/oauth/dialog",
                    flow=OAuthFlowType.IMPLICIT,
                    scopes={
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets",
                    },
                ),
            },
            security=[
                SecurityRequirement("api_key", []),
                SecurityRequirement("petstore_auth", ["write:pets", "read:pets"]),
            ],
        )

    def yaml(self) -> str:
        return """
        swagger: '2.0'
        info:
            title: Cats API
            version: 1.0.0
        paths:
            /api/v1/cats:
                get:
                    responses:
                        '200':
                            description: Gets a list of cats
                    parameters:
                    -   name: page
                        in: query
                        type: integer
                    -   name: size
                        in: query
                        type: integer
                    -   name: search
                        in: query
                        type: string
        securityDefinitions:
            api_key:
                name: api_key
                in: header
                type: apiKey
            petstore_auth:
                flow: implicit
                scopes:
                    write:pets: modify pets in your account
                    read:pets: read your pets
                authorizationUrl: http://swagger.io/api/oauth/dialog
                type: oauth2
        security:
        -   api_key: []
        -   petstore_auth:
            - write:pets
            - read:pets
        """

    def json(self) -> str:
        return """
        {
            "swagger": "2.0",
            "info": {
                "title": "Cats API",
                "version": "1.0.0"
            },
            "paths": {
                "/api/v1/cats": {
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
                                "type": "integer"
                            },
                            {
                                "name": "size",
                                "in": "query",
                                "type": "integer"
                            },
                            {
                                "name": "search",
                                "in": "query",
                                "type": "string"
                            }
                        ]
                    }
                }
            },
            "securityDefinitions": {
                "api_key": {
                    "name": "api_key",
                    "in": "header",
                    "type": "apiKey"
                },
                "petstore_auth": {
                    "flow": "implicit",
                    "scopes": {
                        "write:pets": "modify pets in your account",
                        "read:pets": "read your pets"
                    },
                    "authorizationUrl": "http://swagger.io/api/oauth/dialog",
                    "type": "oauth2"
                }
            },
            "security": [
                {
                    "api_key": []
                },
                {
                    "petstore_auth": [
                        "write:pets",
                        "read:pets"
                    ]
                }
            ]
        }
        """


class OpenAPIExample3(TestItem):
    def get_instance(self) -> Any:
        return OpenAPI(
            info=Info(
                version="1.0.0",
                title="Swagger Petstore",
                description="A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
                terms_of_service="http://swagger.io/terms/",
                contact=Contact(
                    name="Swagger API Team",
                    email="apiteam@swagger.io",
                    url="http://swagger.io",
                ),
                license=License(
                    name="Apache 2.0",
                    url="https://www.apache.org/licenses/LICENSE-2.0.html",
                ),
            ),
            external_docs=ExternalDocs(
                url="https://swagger.io/about", description="find more info here"
            ),
            host="petstore.swagger.io",
            base_path="/api",
            schemes=["http"],
            consumes=["application/json"],
            produces=["application/json"],
            paths={
                "/pets": PathItem(
                    get=Operation(
                        description="Returns all pets from the system that the user has access to",
                        operation_id="findPets",
                        external_docs=ExternalDocs(
                            url="https://swagger.io/about",
                            description="find more info here",
                        ),
                        produces=[
                            "application/json",
                            "application/xml",
                            "text/xml",
                            "text/html",
                        ],
                        parameters=[
                            Parameter(
                                name="tags",
                                in_=ParameterLocation.QUERY,
                                description="tags to filter by",
                                required=False,
                                type=ValueType.ARRAY,
                                items=Items(type=ValueItemType.STRING),
                                collection_format=CollectionFormat.CSV,
                            ),
                            Parameter(
                                name="limit",
                                in_=ParameterLocation.QUERY,
                                description="maximum number of results to return",
                                required=False,
                                type=ValueType.INTEGER,
                                format=ValueFormat.INT32,
                            ),
                        ],
                        responses={
                            "200": Response(
                                description="pet response",
                                schema=Schema(
                                    type=ValueType.ARRAY,
                                    items=Schema(ref="#/definitions/Pet"),
                                ),
                            ),
                            "default": Response(
                                description="unexpected error",
                                schema=Schema(ref="#/definitions/ErrorModel"),
                            ),
                        },
                    ),
                    post=Operation(
                        description="Creates a new pet in the store.  Duplicates are allowed",
                        operation_id="addPet",
                        produces=["application/json"],
                        parameters=[
                            Parameter(
                                name="pet",
                                in_=ParameterLocation.BODY,
                                description="Pet to add to the store",
                                required=True,
                                schema=Schema(ref=get_ref("NewPet")),
                            ),
                        ],
                        responses={
                            "200": Response(
                                description="pet response",
                                schema=Schema(ref=get_ref("Pet")),
                            ),
                            "default": Response(
                                description="unexpected error",
                                schema=Schema(ref="#/definitions/ErrorModel"),
                            ),
                        },
                    ),
                ),
                "/pets/{id}": PathItem(
                    get=Operation(
                        description="Returns a user based on a single ID, if the user does not have access to the pet",
                        operation_id="findPetById",
                        produces=[
                            "application/json",
                            "application/xml",
                            "text/xml",
                            "text/html",
                        ],
                        parameters=[
                            Parameter(
                                name="id",
                                in_=ParameterLocation.PATH,
                                description="ID of pet to fetch",
                                required=True,
                                type=ValueType.INTEGER,
                                format=ValueFormat.INT64,
                            ),
                        ],
                        responses={
                            "200": Response(
                                description="pet response",
                                schema=Schema(ref="#/definitions/Pet"),
                            ),
                            "default": Response(
                                description="unexpected error",
                                schema=Schema(ref="#/definitions/ErrorModel"),
                            ),
                        },
                    ),
                    delete=Operation(
                        description="deletes a single pet based on the ID supplied",
                        operation_id="deletePet",
                        parameters=[
                            Parameter(
                                name="id",
                                in_=ParameterLocation.PATH,
                                description="ID of pet to delete",
                                required=True,
                                type=ValueType.INTEGER,
                                format=ValueFormat.INT64,
                            ),
                        ],
                        responses={
                            "204": Response(description="pet deleted"),
                            "default": Response(
                                description="unexpected error",
                                schema=Schema(ref="#/definitions/ErrorModel"),
                            ),
                        },
                    ),
                ),
            },
            definitions={
                "Pet": Schema(
                    type=ValueType.OBJECT,
                    all_of=[
                        Reference("#/definitions/NewPet"),
                        Schema(
                            required=["id"],
                            properties={
                                "id": Schema(
                                    type=ValueType.INTEGER, format=ValueFormat.INT64
                                )
                            },
                        ),
                    ],
                ),
                "NewPet": Schema(
                    type=ValueType.OBJECT,
                    required=["name"],
                    properties={
                        "name": Schema(type=ValueType.STRING),
                        "tag": Schema(type=ValueType.STRING),
                    },
                ),
                "ErrorModel": Schema(
                    type=ValueType.OBJECT,
                    required=["code", "message"],
                    properties={
                        "code": Schema(
                            type=ValueType.INTEGER, format=ValueFormat.INT32
                        ),
                        "message": Schema(type=ValueType.STRING),
                    },
                ),
            },
        )

    def yaml(self) -> str:
        return """
        swagger: '2.0'
        info:
            title: Swagger Petstore
            version: 1.0.0
            description: A sample API that uses a petstore as an example to demonstrate features
                in the swagger-2.0 specification
            termsOfService: http://swagger.io/terms/
            contact:
                name: Swagger API Team
                url: http://swagger.io
                email: apiteam@swagger.io
            license:
                name: Apache 2.0
                url: https://www.apache.org/licenses/LICENSE-2.0.html
        host: petstore.swagger.io
        basePath: /api
        schemes:
        - http
        consumes:
        - application/json
        produces:
        - application/json
        paths:
            /pets:
                get:
                    responses:
                        '200':
                            description: pet response
                            schema:
                                type: array
                                items:
                                    $ref: '#/definitions/Pet'
                        default:
                            description: unexpected error
                            schema:
                                $ref: '#/definitions/ErrorModel'
                    operationId: findPets
                    produces:
                    - application/json
                    - application/xml
                    - text/xml
                    - text/html
                    description: Returns all pets from the system that the user has access
                        to
                    externalDocs:
                        url: https://swagger.io/about
                        description: find more info here
                    parameters:
                    -   name: tags
                        in: query
                        type: array
                        items:
                            type: string
                        collectionFormat: csv
                        description: tags to filter by
                        required: false
                    -   name: limit
                        in: query
                        type: integer
                        format: int32
                        description: maximum number of results to return
                        required: false
                post:
                    responses:
                        '200':
                            description: pet response
                            schema:
                                $ref: '#/definitions/Pet'
                        default:
                            description: unexpected error
                            schema:
                                $ref: '#/definitions/ErrorModel'
                    operationId: addPet
                    produces:
                    - application/json
                    description: Creates a new pet in the store.  Duplicates are allowed
                    parameters:
                    -   name: pet
                        in: body
                        schema:
                            $ref: '#/definitions/NewPet'
                        description: Pet to add to the store
                        required: true
            /pets/{id}:
                get:
                    responses:
                        '200':
                            description: pet response
                            schema:
                                $ref: '#/definitions/Pet'
                        default:
                            description: unexpected error
                            schema:
                                $ref: '#/definitions/ErrorModel'
                    operationId: findPetById
                    produces:
                    - application/json
                    - application/xml
                    - text/xml
                    - text/html
                    description: Returns a user based on a single ID, if the user does not
                        have access to the pet
                    parameters:
                    -   name: id
                        in: path
                        type: integer
                        format: int64
                        description: ID of pet to fetch
                        required: true
                delete:
                    responses:
                        '204':
                            description: pet deleted
                        default:
                            description: unexpected error
                            schema:
                                $ref: '#/definitions/ErrorModel'
                    operationId: deletePet
                    description: deletes a single pet based on the ID supplied
                    parameters:
                    -   name: id
                        in: path
                        type: integer
                        format: int64
                        description: ID of pet to delete
                        required: true
        definitions:
            Pet:
                type: object
                allOf:
                -   $ref: '#/definitions/NewPet'
                -   required:
                    - id
                    properties:
                        id:
                            type: integer
                            format: int64
            NewPet:
                type: object
                required:
                - name
                properties:
                    name:
                        type: string
                    tag:
                        type: string
            ErrorModel:
                type: object
                required:
                - code
                - message
                properties:
                    code:
                        type: integer
                        format: int32
                    message:
                        type: string
        externalDocs:
            url: https://swagger.io/about
            description: find more info here
        """

    def json(self) -> str:
        return """
        {
            "swagger": "2.0",
            "info": {
                "title": "Swagger Petstore",
                "version": "1.0.0",
                "description": "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification",
                "termsOfService": "http://swagger.io/terms/",
                "contact": {
                    "name": "Swagger API Team",
                    "url": "http://swagger.io",
                    "email": "apiteam@swagger.io"
                },
                "license": {
                    "name": "Apache 2.0",
                    "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
                }
            },
            "host": "petstore.swagger.io",
            "basePath": "/api",
            "schemes": [
                "http"
            ],
            "consumes": [
                "application/json"
            ],
            "produces": [
                "application/json"
            ],
            "paths": {
                "/pets": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "pet response",
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/Pet"
                                    }
                                }
                            },
                            "default": {
                                "description": "unexpected error",
                                "schema": {
                                    "$ref": "#/definitions/ErrorModel"
                                }
                            }
                        },
                        "operationId": "findPets",
                        "produces": [
                            "application/json",
                            "application/xml",
                            "text/xml",
                            "text/html"
                        ],
                        "description": "Returns all pets from the system that the user has access to",
                        "externalDocs": {
                            "url": "https://swagger.io/about",
                            "description": "find more info here"
                        },
                        "parameters": [
                            {
                                "name": "tags",
                                "in": "query",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "collectionFormat": "csv",
                                "description": "tags to filter by",
                                "required": false
                            },
                            {
                                "name": "limit",
                                "in": "query",
                                "type": "integer",
                                "format": "int32",
                                "description": "maximum number of results to return",
                                "required": false
                            }
                        ]
                    },
                    "post": {
                        "responses": {
                            "200": {
                                "description": "pet response",
                                "schema": {
                                    "$ref": "#/definitions/Pet"
                                }
                            },
                            "default": {
                                "description": "unexpected error",
                                "schema": {
                                    "$ref": "#/definitions/ErrorModel"
                                }
                            }
                        },
                        "operationId": "addPet",
                        "produces": [
                            "application/json"
                        ],
                        "description": "Creates a new pet in the store.  Duplicates are allowed",
                        "parameters": [
                            {
                                "name": "pet",
                                "in": "body",
                                "schema": {
                                    "$ref": "#/definitions/NewPet"
                                },
                                "description": "Pet to add to the store",
                                "required": true
                            }
                        ]
                    }
                },
                "/pets/{id}": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "pet response",
                                "schema": {
                                    "$ref": "#/definitions/Pet"
                                }
                            },
                            "default": {
                                "description": "unexpected error",
                                "schema": {
                                    "$ref": "#/definitions/ErrorModel"
                                }
                            }
                        },
                        "operationId": "findPetById",
                        "produces": [
                            "application/json",
                            "application/xml",
                            "text/xml",
                            "text/html"
                        ],
                        "description": "Returns a user based on a single ID, if the user does not have access to the pet",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "type": "integer",
                                "format": "int64",
                                "description": "ID of pet to fetch",
                                "required": true
                            }
                        ]
                    },
                    "delete": {
                        "responses": {
                            "204": {
                                "description": "pet deleted"
                            },
                            "default": {
                                "description": "unexpected error",
                                "schema": {
                                    "$ref": "#/definitions/ErrorModel"
                                }
                            }
                        },
                        "operationId": "deletePet",
                        "description": "deletes a single pet based on the ID supplied",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "type": "integer",
                                "format": "int64",
                                "description": "ID of pet to delete",
                                "required": true
                            }
                        ]
                    }
                }
            },
            "definitions": {
                "Pet": {
                    "type": "object",
                    "allOf": [
                        {
                            "$ref": "#/definitions/NewPet"
                        },
                        {
                            "required": [
                                "id"
                            ],
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int64"
                                }
                            }
                        }
                    ]
                },
                "NewPet": {
                    "type": "object",
                    "required": [
                        "name"
                    ],
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "tag": {
                            "type": "string"
                        }
                    }
                },
                "ErrorModel": {
                    "type": "object",
                    "required": [
                        "code",
                        "message"
                    ],
                    "properties": {
                        "code": {
                            "type": "integer",
                            "format": "int32"
                        },
                        "message": {
                            "type": "string"
                        }
                    }
                }
            },
            "externalDocs": {
                "url": "https://swagger.io/about",
                "description": "find more info here"
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
            schema=Schema(type=ValueType.STRING),
            examples={"text/plain": "Hello, World"},
        )

    def yaml(self) -> str:
        return """
        description: A simple string response
        schema:
            type: string
        examples:
            text/plain: Hello, World
        """

    def json(self) -> str:
        return """
        {
            "description": "A simple string response",
            "schema": {
                "type": "string"
            },
            "examples": {
                "text/plain": "Hello, World"
            }
        }
        """


class ResponseExample2(TestItem):
    def get_instance(self) -> Any:
        return Response(
            description="A simple string response",
            schema=Schema(type=ValueType.STRING),
            headers={
                "X-Foo": Header(
                    description="Some response header", type=HeaderType.STRING
                ),
                "X-Rate-Limit-Limit": Header(
                    description="The number of allowed requests in the current period",
                    type=HeaderType.INTEGER,
                ),
            },
        )

    def yaml(self) -> str:
        return """
        description: A simple string response
        headers:
            X-Foo:
                type: string
                description: Some response header
            X-Rate-Limit-Limit:
                type: integer
                description: The number of allowed requests in the current period
        schema:
            type: string
        """

    def json(self) -> str:
        return """
        {
            "description": "A simple string response",
            "headers": {
                "X-Foo": {
                    "type": "string",
                    "description": "Some response header"
                },
                "X-Rate-Limit-Limit": {
                    "type": "integer",
                    "description": "The number of allowed requests in the current period"
                }
            },
            "schema": {
                "type": "string"
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
        debug_result("v2", example, result, Format.YAML)
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
        debug_result("v2", example, result, Format.JSON)
        raise ae


@pytest.mark.parametrize("example_type", TestItem.__subclasses__())
def test_equality(example_type: Type[TestItem]) -> None:
    example = example_type()
    one = example.get_instance()
    two = example.get_instance()
    assert one == two


@pytest.mark.parametrize(
    "value,expected_result",
    [("one", "#/definitions/one"), (Contact, "#/definitions/Contact")],
)
def test_get_ref(value, expected_result):
    assert get_ref(value) == expected_result
