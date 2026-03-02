"""
Tests for OpenAPI 3.1.x compatibility.

OAS 3.1 introduces several breaking changes compared to 3.0:
  - `type` can be a list (e.g. ["string", "null"]) instead of only a string
  - `nullable: true` is replaced by including "null" in the type list
  - `paths` is optional (valid to have webhooks-only specs)
  - New keywords: const, if/then/else, prefixItems, unevaluatedProperties, $defs
  - exclusiveMinimum / exclusiveMaximum are now numeric values (not booleans)
  - `not` takes a single schema (not a list)
"""

import pytest

from openapidocs.mk.common import is_array_schema, is_object_schema
from openapidocs.mk.jinja import get_primary_type, get_type_display, is_nullable_schema
from openapidocs.mk.v3 import OpenAPIV3DocumentationHandler
from openapidocs.mk.v3.examples import get_example_from_schema
from openapidocs.v3 import Components, Info, OpenAPI, Schema, ValueType
from tests.common import get_file_yaml, get_resource_file_path

# ---------------------------------------------------------------------------
# Helper function unit tests
# ---------------------------------------------------------------------------


class TestGetPrimaryType:
    def test_string(self):
        assert get_primary_type("string") == "string"

    def test_list_single_type(self):
        assert get_primary_type(["string"]) == "string"

    def test_list_nullable(self):
        assert get_primary_type(["string", "null"]) == "string"

    def test_list_nullable_null_first(self):
        assert get_primary_type(["null", "integer"]) == "integer"

    def test_list_only_null(self):
        assert get_primary_type(["null"]) == "null"

    def test_list_multi_type(self):
        # returns the first non-null type
        assert get_primary_type(["string", "integer"]) == "string"

    def test_none_returns_none(self):
        assert get_primary_type(None) is None

    def test_empty_list_returns_none(self):
        assert get_primary_type([]) is None


class TestIsNullableSchema:
    def test_oas30_nullable_true(self):
        assert is_nullable_schema({"type": "string", "nullable": True}) is True

    def test_oas31_null_in_list(self):
        assert is_nullable_schema({"type": ["string", "null"]}) is True

    def test_not_nullable_string(self):
        assert is_nullable_schema({"type": "string"}) is False

    def test_not_nullable_list(self):
        assert is_nullable_schema({"type": ["string", "integer"]}) is False

    def test_non_dict_returns_false(self):
        assert is_nullable_schema(None) is False
        assert is_nullable_schema("string") is False


class TestGetTypeDisplay:
    def test_string(self):
        assert get_type_display("string") == "string"

    def test_list_nullable(self):
        assert get_type_display(["string", "null"]) == "string | null"

    def test_list_multi_type(self):
        assert get_type_display(["string", "integer"]) == "string | integer"

    def test_list_three_types(self):
        assert (
            get_type_display(["string", "integer", "null"]) == "string | integer | null"
        )

    def test_none_returns_empty(self):
        assert get_type_display(None) == ""

    def test_empty_list_returns_empty(self):
        assert get_type_display([]) == ""


# ---------------------------------------------------------------------------
# is_object_schema / is_array_schema with OAS 3.1 list types
# ---------------------------------------------------------------------------


class TestIsObjectSchema:
    def test_oas30_string_type(self):
        assert is_object_schema({"type": "object", "properties": {"x": {}}}) is True

    def test_oas31_list_type(self):
        assert (
            is_object_schema({"type": ["object", "null"], "properties": {"x": {}}})
            is True
        )

    def test_no_properties(self):
        assert is_object_schema({"type": ["object", "null"]}) is False

    def test_different_type(self):
        assert is_object_schema({"type": ["string", "null"]}) is False


class TestIsArraySchema:
    def test_oas30_string_type(self):
        assert is_array_schema({"type": "array", "items": {"type": "string"}}) is True

    def test_oas31_list_type(self):
        assert (
            is_array_schema({"type": ["array", "null"], "items": {"type": "string"}})
            is True
        )

    def test_no_items(self):
        assert is_array_schema({"type": ["array", "null"]}) is False

    def test_different_type(self):
        assert is_array_schema({"type": ["string", "null"]}) is False


# ---------------------------------------------------------------------------
# get_example_from_schema with OAS 3.1 list types
# ---------------------------------------------------------------------------


class TestGetExampleFromSchemaOas31:
    @pytest.mark.parametrize(
        "schema, expected",
        [
            ({"type": ["string", "null"]}, "string"),
            ({"type": ["integer", "null"]}, 0),
            ({"type": ["boolean", "null"]}, True),
            ({"type": ["number", "null"]}, 10.12),
            (
                {"type": ["array", "null"], "items": {"type": "string"}},
                ["string"],
            ),
            (
                {
                    "type": ["object", "null"],
                    "properties": {"x": {"type": "string"}},
                },
                {"x": "string"},
            ),
        ],
    )
    def test_list_type(self, schema, expected):
        assert get_example_from_schema(schema) == expected

    def test_null_only_type(self):
        assert get_example_from_schema({"type": ["null"]}) is None


# ---------------------------------------------------------------------------
# OpenAPIV3DocumentationHandler — OAS 3.1 rendering
# ---------------------------------------------------------------------------


class TestOas31DocumentationHandler:
    def test_renders_without_crash_for_list_types(self):
        """Handler must not crash when type is a list."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "/items": {
                    "get": {
                        "parameters": [
                            {
                                "name": "filter",
                                "in": "query",
                                "schema": {"type": ["string", "null"]},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "OK",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            }
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "Item": {
                        "type": ["object", "null"],
                        "properties": {
                            "name": {"type": ["string", "null"]},
                            "tags": {
                                "type": ["array", "null"],
                                "items": {"type": "string"},
                            },
                        },
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert result is not None

    def test_nullable_parameter_shown_correctly(self):
        """Type list with null → type column shows display type, nullable shows Yes."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "/search": {
                    "get": {
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "schema": {"type": ["string", "null"]},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert "string | null" in result
        assert "Yes" in result  # Nullable column

    def test_non_nullable_parameter_shown_correctly(self):
        """Non-nullable type list → nullable shows No."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "/search": {
                    "get": {
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "schema": {"type": "string"},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert "No" in result  # Nullable column

    def test_missing_paths_does_not_crash(self):
        """paths is optional in OAS 3.1 — webhook-only specs must not crash."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Webhooks Only", "version": "1.0.0"},
            # No "paths" key at all
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert result is not None

    def test_webhooks_only_spec(self):
        """A spec with webhooks but no paths must render without error."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Webhook API", "version": "1.0.0"},
            "webhooks": {
                "newOrder": {
                    "post": {
                        "responses": {
                            "200": {"description": "Webhook received successfully"}
                        }
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert result is not None

    def test_object_schema_with_list_type_renders_properties(self):
        """type: ["object", "null"] schema must render its properties table."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {},
            "components": {
                "schemas": {
                    "Pet": {
                        "type": ["object", "null"],
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        # Properties table must be rendered for an object schema
        assert "id" in result
        assert "name" in result

    def test_array_schema_with_list_type_generates_example(self):
        """type: ["array", "null"] schema must produce a valid auto-generated example."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "/things": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "OK",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": ["array", "null"],
                                            "items": {"type": "string"},
                                        }
                                    }
                                },
                            }
                        }
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        example = handler.generate_example_from_schema(
            {"type": ["array", "null"], "items": {"type": "string"}}
        )
        assert example == ["string"]

    def test_full_oas31_yaml_file(self):
        """Full OAS 3.1 YAML file with list types must render without error."""
        example_file_name = "oas31-openapi.yaml"
        data = get_file_yaml(example_file_name)
        handler = OpenAPIV3DocumentationHandler(
            data, source=get_resource_file_path(example_file_name)
        )
        result = handler.write()
        assert result is not None
        assert len(result) > 0

    def test_full_oas31_yaml_nullable_params(self):
        """Parameters with list types render display type and nullable correctly."""
        example_file_name = "oas31-openapi.yaml"
        data = get_file_yaml(example_file_name)
        handler = OpenAPIV3DocumentationHandler(
            data, source=get_resource_file_path(example_file_name)
        )
        result = handler.write()
        # The `q` parameter has type: [string, "null"]
        assert "string | null" in result

    def test_multi_type_parameter(self):
        """type: [string, integer, null] renders all types joined by ' | '."""
        data = {
            "openapi": "3.1.0",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "/search": {
                    "get": {
                        "parameters": [
                            {
                                "name": "id",
                                "in": "query",
                                "schema": {"type": ["string", "integer", "null"]},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
        }
        handler = OpenAPIV3DocumentationHandler(data)
        result = handler.write()
        assert "string | integer | null" in result


# ---------------------------------------------------------------------------
# Schema dataclass — OAS 3.1 fields serialisation
# ---------------------------------------------------------------------------


class TestSchemaOas31Fields:
    def test_const_field(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(const="fixed-value")
        obj = s.to_obj(schema)
        assert obj["const"] == "fixed-value"

    def test_exclusive_maximum_numeric(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(type=ValueType.INTEGER, exclusive_maximum=100.0)
        obj = s.to_obj(schema)
        assert obj["exclusiveMaximum"] == 100.0

    def test_exclusive_minimum_numeric(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(type=ValueType.INTEGER, exclusive_minimum=0.0)
        obj = s.to_obj(schema)
        assert obj["exclusiveMinimum"] == 0.0

    def test_defs_serialised_as_dollar_defs(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(defs={"inner": Schema(type=ValueType.STRING)})
        obj = s.to_obj(schema)
        assert "$defs" in obj
        assert "inner" in obj["$defs"]

    def test_if_then_else(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(
            if_=Schema(type=ValueType.STRING),
            then_=Schema(type=ValueType.STRING, min_length=1),
            else_=Schema(type=ValueType.INTEGER),
        )
        obj = s.to_obj(schema)
        assert "if" in obj
        assert "then" in obj
        assert "else" in obj

    def test_prefix_items(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(
            type=ValueType.ARRAY,
            prefix_items=[
                Schema(type=ValueType.STRING),
                Schema(type=ValueType.INTEGER),
            ],
        )
        obj = s.to_obj(schema)
        assert "prefixItems" in obj
        assert len(obj["prefixItems"]) == 2

    def test_not_is_single_schema(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(not_=Schema(type=ValueType.STRING))
        obj = s.to_obj(schema)
        assert "not" in obj
        assert obj["not"]["type"] == "string"

    def test_type_list_serialised_as_list(self):
        from openapidocs.common import Serializer

        s = Serializer()
        schema = Schema(type=[ValueType.STRING, ValueType.NULL])
        obj = s.to_obj(schema)
        assert obj["type"] == ["string", "null"]

    def test_openapi_root_with_oas31_schema(self):
        from openapidocs.common import Serializer

        s = Serializer()
        doc = OpenAPI(
            info=Info(title="Test", version="1.0.0"),
            components=Components(
                schemas={
                    "NullableString": Schema(type=[ValueType.STRING, ValueType.NULL]),
                    "ConstSchema": Schema(const=42),
                }
            ),
        )
        obj = s.to_obj(doc)
        schemas = obj["components"]["schemas"]
        assert schemas["NullableString"]["type"] == ["string", "null"]
        assert schemas["ConstSchema"]["const"] == 42


# ---------------------------------------------------------------------------
# Version mismatch warnings — OAS 3.1 features in a 3.0.x document
# ---------------------------------------------------------------------------


def _base_doc(version="3.0.3"):
    return {
        "openapi": version,
        "info": {"title": "Test", "version": "1.0"},
        "paths": {},
    }


class TestVersionMismatchWarning:
    def test_no_warning_for_clean_30_doc(self):
        """A 3.0 document with no 3.1 features must not emit a warning."""
        import warnings

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(_base_doc("3.0.3"))
        version_warnings = [w for w in caught if "OAS 3.1-specific" in str(w.message)]
        assert version_warnings == []

    def test_no_warning_for_31_doc_with_31_features(self):
        """A 3.1 document using 3.1 features must not emit a warning."""
        doc = _base_doc("3.1.0")
        doc["components"] = {"schemas": {"Foo": {"type": ["string", "null"]}}}
        import warnings

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(doc)
        version_warnings = [w for w in caught if "OAS 3.1-specific" in str(w.message)]
        assert version_warnings == []

    def test_warning_for_list_type_in_30_doc(self):
        """type as list in a 3.0 doc must trigger a warning."""
        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"type": ["string", "null"]}}}
        with pytest.warns(UserWarning, match="3.0.3"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_mentions_detected_feature(self):
        """Warning message must name the detected 3.1 feature."""
        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"type": ["string", "null"]}}}
        with pytest.warns(UserWarning, match="type as list"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_const_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"type": "string", "const": "fixed"}}}
        with pytest.warns(UserWarning, match="const"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_defs_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"$defs": {"Bar": {"type": "string"}}}}}
        with pytest.warns(UserWarning, match=r"\$defs"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_webhooks_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["webhooks"] = {
            "newOrder": {"post": {"responses": {"200": {"description": "OK"}}}}
        }
        with pytest.warns(UserWarning, match="webhooks"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_if_then_else_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {
            "schemas": {
                "Conditional": {
                    "if": {"type": "string"},
                    "then": {"minLength": 1},
                    "else": {"type": "integer"},
                }
            }
        }
        with pytest.warns(UserWarning, match="if"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_prefix_items_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {
            "schemas": {
                "Tuple": {
                    "type": "array",
                    "prefixItems": [{"type": "string"}, {"type": "integer"}],
                }
            }
        }
        with pytest.warns(UserWarning, match="prefixItems"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_unevaluated_properties_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {
            "schemas": {
                "Strict": {
                    "type": "object",
                    "properties": {"x": {"type": "string"}},
                    "unevaluatedProperties": False,
                }
            }
        }
        with pytest.warns(UserWarning, match="unevaluatedProperties"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_exclusive_maximum_as_number_in_30_doc(self):
        doc = _base_doc("3.0.3")
        doc["components"] = {
            "schemas": {"Score": {"type": "integer", "exclusiveMaximum": 100}}
        }
        with pytest.warns(UserWarning, match="exclusiveMaximum as number"):
            OpenAPIV3DocumentationHandler(doc)

    def test_no_warning_for_exclusive_maximum_as_bool_in_30_doc(self):
        """exclusiveMaximum: true is valid 3.0 syntax and must not trigger a warning."""
        doc = _base_doc("3.0.3")
        doc["components"] = {
            "schemas": {"Score": {"type": "integer", "exclusiveMaximum": True}}
        }
        import warnings

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(doc)
        version_warnings = [w for w in caught if "OAS 3.1-specific" in str(w.message)]
        assert version_warnings == []

    def test_warning_mentions_openapi_version(self):
        """Warning message must include the declared version string."""
        doc = _base_doc("3.0.1")
        doc["components"] = {"schemas": {"Foo": {"type": ["string", "null"]}}}
        with pytest.warns(UserWarning, match="3.0.1"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_suggests_upgrade(self):
        """Warning message must suggest upgrading to 3.1.0."""
        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"type": ["string", "null"]}}}
        with pytest.warns(UserWarning, match="3.1.0"):
            OpenAPIV3DocumentationHandler(doc)


# ---------------------------------------------------------------------------
# OAS 3.0 features in a 3.1 document
# ---------------------------------------------------------------------------


class TestOas30FeaturesIn31Doc:
    def test_no_warning_for_clean_31_doc(self):
        """A 3.1 document with no 3.0 features must not emit an OAS-3.0 warning."""
        import warnings

        doc = _base_doc("3.1.0")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(doc)
        version_warnings = [w for w in caught if "OAS 3.0-specific" in str(w.message)]
        assert version_warnings == []

    def test_no_warning_for_30_doc(self):
        """A 3.0 document must not trigger the OAS-3.0-in-3.1 warning."""
        import warnings

        doc = _base_doc("3.0.3")
        doc["components"] = {"schemas": {"Foo": {"type": "string", "nullable": True}}}
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(doc)
        oas30_in_31 = [w for w in caught if "OAS 3.0-specific" in str(w.message)]
        assert oas30_in_31 == []

    def test_warning_for_nullable_true_in_31_doc(self):
        """`nullable: true` is a 3.0 pattern and must warn in a 3.1 doc."""
        doc = _base_doc("3.1.0")
        doc["components"] = {"schemas": {"Foo": {"type": "string", "nullable": True}}}
        with pytest.warns(UserWarning, match="nullable: true"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_mentions_31_version(self):
        """Warning message must include the declared 3.1.x version."""
        doc = _base_doc("3.1.0")
        doc["components"] = {"schemas": {"Foo": {"type": "string", "nullable": True}}}
        with pytest.warns(UserWarning, match="3.1.0"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_boolean_exclusive_maximum_in_31_doc(self):
        """`exclusiveMaximum: true` (boolean) is a 3.0 pattern and must warn in 3.1."""
        doc = _base_doc("3.1.0")
        doc["components"] = {
            "schemas": {
                "Score": {"type": "integer", "maximum": 100, "exclusiveMaximum": True}
            }
        }
        with pytest.warns(UserWarning, match="exclusiveMaximum: true/false"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_for_boolean_exclusive_minimum_in_31_doc(self):
        """`exclusiveMinimum: true` (boolean) is a 3.0 pattern and must warn in 3.1."""
        doc = _base_doc("3.1.0")
        doc["components"] = {
            "schemas": {
                "Score": {"type": "integer", "minimum": 0, "exclusiveMinimum": True}
            }
        }
        with pytest.warns(UserWarning, match="exclusiveMinimum: true/false"):
            OpenAPIV3DocumentationHandler(doc)

    def test_no_warning_for_numeric_exclusive_maximum_in_31_doc(self):
        """`exclusiveMaximum: 100` (numeric) is valid 3.1 and must not warn."""
        import warnings

        doc = _base_doc("3.1.0")
        doc["components"] = {
            "schemas": {"Score": {"type": "integer", "exclusiveMaximum": 100}}
        }
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            OpenAPIV3DocumentationHandler(doc)
        oas30_in_31 = [w for w in caught if "OAS 3.0-specific" in str(w.message)]
        assert oas30_in_31 == []

    def test_warning_detects_nullable_nested_in_path(self):
        """`nullable: true` nested inside a path operation schema must warn."""
        doc = _base_doc("3.1.0")
        doc["paths"] = {
            "/items": {
                "get": {
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "schema": {"type": "string", "nullable": True},
                        }
                    ],
                    "responses": {"200": {"description": "OK"}},
                }
            }
        }
        with pytest.warns(UserWarning, match="nullable: true"):
            OpenAPIV3DocumentationHandler(doc)

    def test_warning_mentions_not_valid_in_31(self):
        """Warning message must state the feature is not valid in OAS 3.1."""
        doc = _base_doc("3.1.0")
        doc["components"] = {"schemas": {"Foo": {"type": "string", "nullable": True}}}
        with pytest.warns(UserWarning, match="not valid in OAS 3.1"):
            OpenAPIV3DocumentationHandler(doc)
