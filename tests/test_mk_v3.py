import pytest

from openapidocs.mk.v3 import (
    OpenAPIFileNotFoundError,
    OpenAPIV3DocumentationHandler,
    style_from_value,
)
from openapidocs.mk.v3.examples import ObjectExampleHandler
from tests.common import (
    compatible_str,
    get_file_json,
    get_file_yaml,
    get_resource_file_content,
    get_resource_file_path,
)


@pytest.mark.parametrize("example_file", ["example1", "example2", "example3"])
def test_v3_markdown_gen(example_file):
    data = get_file_json(f"{example_file}-openapi.json")
    expected_result = get_resource_file_content(f"{example_file}-output.md")

    handler = OpenAPIV3DocumentationHandler(data)

    html = handler.write()
    assert compatible_str(html, expected_result)


def test_v3_markdown_gen_split_file():
    example_file = "example4-split"
    example_file_name = f"{example_file}-openapi.yaml"
    data = get_file_yaml(example_file_name)
    expected_result = get_resource_file_content(f"{example_file}-output.md")

    handler = OpenAPIV3DocumentationHandler(
        data, source=get_resource_file_path(example_file_name)
    )

    html = handler.write()

    assert compatible_str(html, expected_result)


def test_v3_external_ref_with_fragment():
    """
    Regression test for https://github.com/Neoteroi/essentials-openapi/issues/49
    $ref values of the form 'file.yaml#/path/to/item' should resolve the fragment
    within the external file rather than failing with a file-not-found error.
    """
    source = get_resource_file_path("spec-fragments/openapi.yaml")
    data = get_file_yaml("spec-fragments/openapi.yaml")

    handler = OpenAPIV3DocumentationHandler(data, source=source)
    output = handler.write()

    # Parameters resolved from types.yaml#/components/parameters/...
    assert "<code>page</code>" in output
    assert "<code>size</code>" in output
    # Response resolved from types.yaml#/components/responses/SearchResponse
    assert '=== "200 OK"' in output
    assert '"total"' in output


def test_file_ref_raises_for_missing_file():
    with pytest.raises(OpenAPIFileNotFoundError):
        OpenAPIV3DocumentationHandler(
            {
                "openapi": "3.0.0",
                "info": {"title": "Split Public API"},
                "components": {"schemas": {"$ref": "./not-existing.yml"}},
            }
        )


def test_swagger2_raises_not_supported():
    """
    Regression test for https://github.com/Neoteroi/essentials-openapi/issues/30
    Swagger 2.0 specs should raise a clear ValueError instead of silently
    producing empty output.
    """
    with pytest.raises(
        ValueError, match="Swagger 2.0 specifications are not supported"
    ):
        OpenAPIV3DocumentationHandler({"swagger": "2.0", "info": {}, "paths": {}})


def test_v3_response_header_ref():
    """
    Regression test for https://github.com/Neoteroi/essentials-openapi/issues/60
    Response headers that use $ref to #/components/headers/... should be resolved
    without raising an UndefinedError.
    """
    data = get_file_yaml("example9-openapi.yaml")
    handler = OpenAPIV3DocumentationHandler(data)
    output = handler.write()

    assert "Current-Page" in output
    assert "The current page of total pages this response represents." in output
    assert "X-Rate-Limit" in output
    assert "Rate limit per hour" in output


@pytest.mark.parametrize(
    "input,expected_result",
    [
        (
            {
                "text/plain": {"schema": {"$ref": "#/components/schemas/Release"}},
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Release"}
                },
                "text/json": {"schema": {"$ref": "#/components/schemas/Release"}},
            },
            {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Release"},
                    "alt_types": ["text/json", "text/plain"],
                }
            },
        ),
        (
            {
                "text/xml": {"schema": {"$ref": "#/components/schemas/Release"}},
                "application/xml": {"schema": {"$ref": "#/components/schemas/Release"}},
                "xml": {"schema": {"$ref": "#/components/schemas/Release"}},
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Release"}
                },
            },
            {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Release"}
                },
                "application/xml": {
                    "schema": {"$ref": "#/components/schemas/Release"},
                    "alt_types": ["text/xml", "xml"],
                },
            },
        ),
    ],
)
def test_v3_simplify_content(input, expected_result):
    handler = OpenAPIV3DocumentationHandler({})

    result = handler.simplify_content(input)
    assert result == expected_result


def test_get_empty_schemas():
    handler = OpenAPIV3DocumentationHandler({})

    assert list(handler.get_schemas()) == []


def test_get_properties_missing_data():
    handler = OpenAPIV3DocumentationHandler({})

    properties = handler.get_properties({"$ref": "#/components/schemas/Foo"})
    assert properties == []


def test_expand_references_ref():
    handler = OpenAPIV3DocumentationHandler(
        {
            "components": {
                "schemas": {
                    "Foo": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "ufo": {"$ref": "#/components/schemas/Ufo"},
                        },
                    },
                    "Ufo": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "name": {"type": "string"},
                        },
                    },
                }
            }
        }
    )

    exp = handler.expand_references({"$ref": "#/components/schemas/Foo"})
    assert exp == {
        "type": "object",
        "properties": {
            "id": {"type": "string", "format": "uuid"},
            "ufo": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                },
            },
        },
    }


def test_generate_example_from_schema_empty():
    handler = OpenAPIV3DocumentationHandler({})

    assert handler.generate_example_from_schema({}) is None


def test_write_content_schema_empty():
    handler = OpenAPIV3DocumentationHandler({})

    assert handler.write_content_schema({}) == ""


def test_get_content_examples():
    handler = OpenAPIV3DocumentationHandler({})

    examples = list(
        handler.get_content_examples(
            {
                "examples": {
                    "one": "Lorem ipsum",
                    "two": {"value": {"a": 1, "b": 2, "c": 3}},
                }
            }
        )
    )

    assert examples[0].value == "Lorem ipsum"
    assert examples[1].value == {"a": 1, "b": 2, "c": 3}


def test_get_parameters_for_security_default():
    handler = OpenAPIV3DocumentationHandler({})

    assert handler.get_parameter_for_security("Foo", {"type": "foo"}) == {
        "name": "Foo",
        "in": "header",
        "description": "",
        "schema": {
            "type": "string",
            "default": "N/A",
            "nullable": False,
        },
    }


def test_iter_bindings():
    handler = OpenAPIV3DocumentationHandler(get_file_json("example1-openapi.json"))

    values = list(handler.iter_schemas_bindings())

    assert values == [
        ("Category", "Release"),
        ("CreateOrganizationsBoundInput", "OrganizationBoundInput"),
        ("ProfessionalContext", "ProfessionalMembership"),
        ("Release", "Category"),
        ("Release", "ReleaseCountry"),
        ("Release", "ReleaseHistory"),
        ("Release", "ReleaseNode"),
        ("Release", "ReleaseOrganization"),
        ("ReleaseCountry", "Country"),
        ("ReleaseCountry", "Release"),
        ("ReleaseHistory", "Release"),
        ("ReleaseNode", "NodeInfo"),
        ("ReleaseNode", "Release"),
        ("ReleaseNodeDownload", "NodeInfo"),
        ("ReleaseNodeDownload", "Release"),
        ("ReleaseNodeDownloadPaginatedSet", "ReleaseNodeDownload"),
        ("ReleaseOrganization", "Release"),
        ("ReleasePaginatedSet", "Release"),
    ]


def test_iter_bindings_arrays():
    handler = OpenAPIV3DocumentationHandler(
        {
            "components": {
                "schemas": {
                    "Pet": {
                        "type": "object",
                        "required": ["id", "name"],
                        "properties": {
                            "id": {"type": "integer", "format": "int64"},
                            "name": {"type": "string"},
                            "tag": {"type": "string"},
                            "category": {
                                "type": "string",
                                "enum": ["One", "Two", "Three"],
                            },
                        },
                    },
                    "Pets": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Pet"},
                    },
                }
            }
        }
    )

    values = list(handler.iter_schemas_bindings())

    assert values == [("Pets", "Pet")]


def test_style_from_value_raises_value_error():
    with pytest.raises(ValueError):
        style_from_value("WRONG")


def test_v3_markdown_gen_handles_missing_components():
    data = {
        "openapi": "3.0.0",
        "info": {
            "version": "1.0.0",
            "title": "Example",
        },
        "paths": {
            "/foo": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Foo",
                            "content": {"text/plain": {"schema": {"type": "string"}}},
                        },
                    },
                },
            },
        },
    }
    handler = OpenAPIV3DocumentationHandler(data)

    html = handler.write()
    assert html is not None


def test_object_example_handler_handles_missing_pros():
    handler = ObjectExampleHandler()

    assert handler.get_example({}) == {}


@pytest.mark.parametrize("example_file", ["example6", "example7", "example8"])
def test_v3_markdown_yaml(example_file):
    # example6
    # https://github.com/Neoteroi/essentials-openapi/issues/21

    # example7
    # https://github.com/Neoteroi/essentials-openapi/issues/24

    # example8
    # https://github.com/Neoteroi/mkdocs-plugins/issues/5#issuecomment-2741388516
    example_file_name = f"{example_file}-openapi.yaml"
    data = get_file_yaml(example_file_name)
    expected_result = get_resource_file_content(f"{example_file}-output.md")

    handler = OpenAPIV3DocumentationHandler(
        data, source=get_resource_file_path(example_file_name)
    )

    html = handler.write()

    compatible_str(html, expected_result)


@pytest.mark.parametrize("example_file", ["example8"])
def test_v3_markdown_yaml_plain_markdown(example_file):
    # example8
    # https://github.com/Neoteroi/mkdocs-plugins/issues/5#issuecomment-2741388516
    example_file_name = f"{example_file}-openapi.yaml"
    data = get_file_yaml(example_file_name)
    expected_result = get_resource_file_content(f"{example_file}-output-plain.md")

    handler = OpenAPIV3DocumentationHandler(
        data, source=get_resource_file_path(example_file_name), style="MARKDOWN"
    )

    html = handler.write()

    compatible_str(html, expected_result)
