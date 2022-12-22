"""
This module provides functions to generate Markdown for OpenAPI Version 3.
"""
import copy
import os
import warnings
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

from openapidocs.logs import logger
from openapidocs.mk import read_dict, sort_dict
from openapidocs.mk.common import (
    DocumentsWriter,
    get_ref_type_name,
    is_array_schema,
    is_object_schema,
    is_reference,
)
from openapidocs.mk.contents import ContentWriter, FormContentWriter, JSONContentWriter
from openapidocs.mk.jinja import Jinja2DocumentsWriter, OutputStyle
from openapidocs.mk.texts import EnglishTexts, Texts
from openapidocs.mk.v3.examples import get_example_from_schema
from openapidocs.utils.source import read_from_source


def _can_simplify_json(content_type) -> bool:
    return "json" in content_type or content_type == "text/plain"


def _can_simplify_xml(content_type) -> bool:
    return "xml" in content_type


class ExpandContext:
    def __init__(self) -> None:
        self.expanded_refs = set()


@dataclass
class ContentExample:
    value: Any
    auto_generated: bool
    name: str = ""


def style_from_value(value: Union[int, str]) -> OutputStyle:
    if isinstance(value, int) or value.isdigit():
        return OutputStyle(int(value))
    try:
        return OutputStyle[value]
    except KeyError:
        raise ValueError(f"Invalid style: {value}")


class OpenAPIDocumentationHandlerError(Exception):
    """Base type for exceptions raised by the handler generating documentation."""


class OpenAPIFileNotFoundError(OpenAPIDocumentationHandlerError, FileNotFoundError):
    """
    Exception raised when a $ref property pointing to a file (to split OAD specification
    into multiple files) is not found.
    """

    def __init__(self, reference: str, attempted_path: Path) -> None:
        super().__init__(
            f"Cannot resolve the $ref source {reference} "
            f"Tried to read from path: {attempted_path}"
        )


class OpenAPIV3DocumentationHandler:
    """
    Class that produces documentation from OpenAPI Documentation V3.
    """

    simplifiable_types = {
        "application/json": _can_simplify_json,
        "application/xml": _can_simplify_xml,
    }

    content_writers: List[ContentWriter] = [
        JSONContentWriter(),
        FormContentWriter(),
    ]

    default_content_writer = JSONContentWriter()

    def __init__(
        self,
        doc,
        texts: Optional[Texts] = None,
        writer: Optional[DocumentsWriter] = None,
        style: Union[int, str] = 1,
        source: str = "",
    ) -> None:
        self._source = source
        self.texts = texts or EnglishTexts()
        self._writer = writer or Jinja2DocumentsWriter(
            __name__, views_style=style_from_value(style)
        )
        self.doc = self.normalize_data(copy.deepcopy(doc))

    @property
    def source(self) -> str:
        return self._source

    def normalize_data(self, data):
        """
        Applies corrections to the OpenAPI specification, to simplify its handling.

        This method also resolves references to different files, if the root is split
        into multiple files.

        ---
        Ref.
        An OpenAPI document MAY be made up of a single document or be divided into
        multiple, connected parts at the discretion of the user. In the latter case,
        $ref fields MUST be used in the specification to reference those parts as
        follows from the JSON Schema definitions.
        """
        if "components" not in data:
            data["components"] = {}

        return self._transform_data(
            data, Path(self.source).parent if self.source else Path.cwd()
        )

    def _transform_data(self, obj, source_path):
        if not isinstance(obj, dict):
            return obj

        if "$ref" in obj:
            return self._handle_obj_ref(obj, source_path)

        clone = {}

        for key, value in obj.items():
            if isinstance(value, list):
                clone[key] = [self._transform_data(item, source_path) for item in value]
            elif isinstance(value, dict):
                clone[key] = self._handle_obj_ref(value, source_path)
            else:
                clone[key] = self._transform_data(value, source_path)

        return clone

    def _handle_obj_ref(self, obj, source_path):
        """
        Handles a dictionary containing a $ref property, resolving the reference if it
        is to a file. This is used to read specification files when they are split into
        multiple items.
        """
        assert isinstance(obj, dict)
        if "$ref" in obj:
            reference = obj["$ref"]
            if isinstance(reference, str) and not reference.startswith("#/"):
                referred_file = Path(os.path.abspath(source_path / reference))

                if referred_file.exists():
                    logger.debug("Handling $ref source: %s", reference)
                else:
                    raise OpenAPIFileNotFoundError(reference, referred_file)
                sub_fragment = read_from_source(str(referred_file))
                return self._transform_data(sub_fragment, referred_file.parent)
            else:
                return obj
        return self._transform_data(obj, source_path)

    def get_operations(self):
        """
        Gets a dictionary of operations grouped by tag.
        """
        data = self.doc
        groups = defaultdict(list)
        paths = data["paths"]

        for path, path_item in paths.items():
            tag = self.get_tag(path_item) or ""
            groups[tag].append((path, path_item))

        return groups

    def get_schemas(self):
        schemas = read_dict(self.doc, "components", "schemas")

        if not schemas:
            return

        yield from sort_dict(schemas)

    def get_tag(self, path_item) -> Optional[str]:
        """
        Tries to obtain a single tag for all operations inside a given path item.
        See https://spec.openapis.org/oas/v3.1.0#path-item-object

        A path item looks like this:

        {
            "get": {..., "tags": ["Albums"]},
            "post": {..., "tags": ["Albums"]}
        }

        Tags are optional.
        """
        single_tag: Optional[str] = None

        for operation in path_item.values():
            tags = operation.get("tags")

            if not tags:
                continue

            single_tag = next(
                (item for item in tags if single_tag is None or item == single_tag),
                None,
            )

        return single_tag

    def simplify_content(self, content):
        """
        Gets a copy of the content definition, altered to be more concise, when several
        content types can be used to describe the same schema, returning a dictionary of
        references and possible content-types.

        Example:

        {
            "text/plain": {
                "schema": {
                    "$ref": "#/components/schemas/Release"
                }
            },
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Release"
                }
            },
            "text/json": {
                "schema": {
                    "$ref": "#/components/schemas/Release"
                }
            }
        }

        ->

        {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Release"
                },
                "alt_types": ["text/plain", "text/json"]
            }
        }
        """
        simplified_content = copy.deepcopy(content)
        all_types = simplified_content.keys()

        for content_type, predicate in self.simplifiable_types.items():
            main_declaration = simplified_content.get(content_type)

            if main_declaration:
                types_to_remove = {
                    other_type
                    for other_type in all_types
                    if predicate(other_type)
                    and other_type != content_type
                    and simplified_content[other_type] == main_declaration
                }

                for type_to_remove in types_to_remove:
                    del simplified_content[type_to_remove]

                if types_to_remove:
                    alt_types = list(types_to_remove)
                    # sort to use alphabetically sorted values
                    alt_types.sort()
                    main_declaration["alt_types"] = alt_types

        return simplified_content

    def get_security_scheme(self, name: str) -> dict:
        """
        Gets a security scheme from the components section, by name.
        """
        security_scheme = read_dict(self.doc, "components", "securitySchemes")

        if not security_scheme:  # pragma: no cover
            warnings.warn(
                "Missing section in components. A security scheme referenced "
                "in a path item is not configured."
            )
            return {}

        if name not in security_scheme:  # pragma: no cover
            warnings.warn(
                f'Missing security scheme definition "{name}". '
                "A path item references this scheme, but it is not configured "
                "in components.securitySchemes."
            )
            return {}
        return security_scheme[name]

    def get_parameter_for_security(self, key: str, security_scheme: dict):
        """
        The OpenAPI Documentation specification is messy. The security scheme objects
        describe input parameters in a completely different way than input parameters,
        and try to cover too many scenarios (OAuth flows).

        https://swagger.io/specification/#security-scheme-object
        https://swagger.io/specification/#security-requirement-object
        """
        security_type = security_scheme.get("type")

        if security_type == "http":
            scheme = security_scheme.get("scheme")

            description = ""
            if scheme == "bearer":
                description = "JWT Bearer token"
            elif scheme == "basic":
                description = "Basic authentication"

            return {
                "name": key,
                "in": "header",
                "description": security_scheme.get("description", description),
                "schema": {"type": "string", "default": "N/A", "nullable": False},
            }
        if security_type == "apiKey":
            return {
                "name": key,
                "in": security_scheme.get("in"),
                "description": security_scheme.get("description", "API key"),
                "schema": {"type": "string", "default": "N/A", "nullable": False},
            }

        return {
            "name": key,
            "in": "header",
            "description": security_scheme.get("description", ""),
            "schema": {
                "type": "string",
                "default": "N/A",
                "nullable": False,
            },
        }

    def get_operation_security(self, operation):
        """
        Returns security definition for an operation. This can come from global settings
        or from specific settings.

        Example:
            security:
                - ApiKeyAuth: []
                - OAuth2: [read, write]

            Refer to:

            https://swagger.io/specification/#security-scheme-object
            https://swagger.io/specification/#security-requirement-object
        """
        for source in [operation, self.doc]:
            if "security" in source:
                return source["security"]
        return None

    def _resolve_opt_ref(self, obj):
        if "$ref" in obj:
            return self.resolve_reference(obj)
        return obj

    def get_parameters(self, operation) -> List[dict]:
        """
        Returns a list of objects describing the input parameters for a given operation.
        References to #/components/parameters are resolved, to show the information in
        a single place.
        """
        parameters = [
            self._resolve_opt_ref(item) for item in operation.get("parameters", [])
        ]

        results = [
            param
            for param in sorted(
                parameters,
                key=lambda x: x["name"].lower() if (x and "name" in x) else "",
            )
            if param
        ]

        security_options = self.get_operation_security(operation)
        if security_options:
            # The OAD specification here is messy and confusing: it treats input
            # parameters for authentication like they were a completely different thing
            # than other input parameters - which in most cases is not true
            # (Authorization headers, cookies, API Keys in headers, etc.).

            # Here we prepend the parameter for authentication | authorization,
            # so that readers who are not expert of various authentication methods can
            # see that a certain header / parameter is needed.
            assert isinstance(security_options, list)
            for option in security_options:
                for key in option.keys():
                    # TODO: support for showing scopes
                    scheme = self.get_security_scheme(key)
                    results.insert(0, self.get_parameter_for_security(key, scheme))

        return results

    def write(self) -> str:
        return self._writer.write(
            self.doc,
            operations=self.get_operations(),
            texts=self.texts,
            handler=self,
        )

    def get_content_examples(self, data) -> Iterable[ContentExample]:
        """
        Returns examples to show an example for a content definition.
        The specification allows several options: examples, example, objects, raw
        strings. If no example is specified, this method generates one automatically
        from the schema definition.

        Example (YAML):

        requestBody:
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/CreateCatInput'
                    examples:
                        fat_cat:
                            value:
                                name: Fatty
                                active: false
                                type: european
                        thin_cat:
                            value:
                                name: Thinny
                                active: false
                                type: persian
            required: true
            description: Example description etc. etc.


        responses:
            '200':
                description: A cat
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Cat'
                        example:
                            id: 3fa85f64-5717-4562-b3fc-2c963f66afa6
                            name: Foo
                            active: true
                            type: european
                            creation_time: '2020-10-25T19:39:31.751652'
        """
        examples = data.get("examples")

        if examples:
            for example_name, definition in examples.items():
                if isinstance(definition, str):
                    value = definition
                elif is_reference(definition):
                    value = self.resolve_reference(definition)
                else:
                    value = definition.get("value")
                yield ContentExample(value, False, example_name)

        example = data.get("example")
        auto_generated = False

        if not example and not examples:
            # try to generate a basic example from the schema, on the fly
            example = self.generate_example_from_schema(data.get("schema"))
            auto_generated = True

        if example:
            yield ContentExample(example, auto_generated)

        return ""

    def write_content_example(self, example: ContentExample, content_type: str) -> str:
        example_handler = self.get_content_writer(content_type)
        return example_handler.write(example.value)

    def generate_example_from_schema(self, schema) -> Any:
        if not schema:
            return None

        if is_reference(schema):
            schema = self.resolve_reference(schema["$ref"])

        return get_example_from_schema(self.expand_references(schema))

    def write_content_schema(self, data) -> str:
        schema = data.get("schema")

        if not schema:
            return ""

        if is_reference(schema):
            schema = self.resolve_reference(schema["$ref"])

        return self.default_content_writer.write(schema)

    def resolve_reference(self, reference: Union[str, dict]) -> Any:
        """
        Returns the schema object from the components, by reference ($ref).
        """
        if isinstance(reference, dict):
            reference = reference["$ref"]
        assert isinstance(reference, str)
        return read_dict(self.doc, *reference.lstrip("#/").split("/"))

    def expand_references(self, schema, context: Optional[ExpandContext] = None):
        """
        Returns a clone of the given schema object, in which all $ref properties are
        resolved and made verbose. This is to provide a better view of schemas that does
        not require navigating to different parts of the documentation.

        This method handles recursive references setting `null` values.
        """
        if context is None:
            context = ExpandContext()

        if is_reference(schema):
            return self.expand_references(self.resolve_reference(schema))

        if schema is None:
            # this should not happen, but we don't want the whole build to fail
            return None

        clone = copy.deepcopy(schema)

        for key in list(clone.keys()):
            value = clone[key]

            if is_reference(value):
                ref = value["$ref"]
                if ref in context.expanded_refs:
                    clone[key] = None
                else:
                    context.expanded_refs.add(ref)

                    resolved_ref = self.resolve_reference(value)

                    if resolved_ref is None:  # pragma: no cover
                        logger.warning(
                            "Cannot resolve the reference %s. "
                            "Is a fragment missing from `components` object?",
                            value,
                        )
                        clone[key] = {}
                    else:
                        clone[key] = self.expand_references(resolved_ref, context)
            elif isinstance(value, dict):
                if is_array_schema(value) and is_reference(value["items"]):
                    ref = value["items"]["$ref"]
                    if ref in context.expanded_refs:
                        clone[key] = None
                        continue

                clone[key] = self.expand_references(value, context)
            else:
                clone[key] = value

        return clone

    def get_content_writer(self, content_type: str) -> ContentWriter:
        """
        Returns a ContentWriter to create a markdown representation of the given
        content type. If none specific is available, it returns the
        `default_content_writer` bound to this class.
        """
        return next(
            (
                writer
                for writer in self.content_writers
                if writer.handle_content_type(content_type)
            ),
            self.default_content_writer,
        )

    def get_properties(self, schema):
        if is_reference(schema):
            schema = self.resolve_reference(schema)

            if not schema:
                return []

        return [[key, value] for key, value in sort_dict(schema.get("properties", {}))]

    def iter_schemas_bindings(self):
        """
        Iterates through components schemas and yields tuples of type names and their
        $refs types.
        """
        schemas = self.get_schemas()

        for type_name, schema in schemas:
            if is_object_schema(schema):
                for _, prop_schema in sort_dict(schema["properties"]):
                    if is_reference(prop_schema):
                        yield type_name, get_ref_type_name(prop_schema)

                    if is_array_schema(prop_schema) and is_reference(
                        prop_schema["items"]
                    ):
                        yield type_name, get_ref_type_name(prop_schema["items"])

            if is_array_schema(schema) and is_reference(schema["items"]):
                yield type_name, get_ref_type_name(schema["items"])
