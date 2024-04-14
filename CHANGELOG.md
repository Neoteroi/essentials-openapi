# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.10] - 2024-04-14
- Fixes `MARKDOWN` style not creating tables using the minimum 3 hyphens,
  reported by @michael-nok.
- Adds support for displaying descriptions of schema
  properties, requested by @Maia-Everett.

## [1.0.9] - 2023-11-20
- Adds support for Python 3.12.
- Adds `MarkupSafe` among required dependencies (and not optional).
- Adds support for latest function `model_dump` in Pydantic 2 (for examples
  defined using Pydantic models).
- Upgrades development dependencies.
- Fix bug with missing items entry #36 by @mh7d and @mh-at-fujitsu

## [1.0.8] - 2023-07-19 :cat:
- Fixes example generation breaks on explicitly enumerated array elements #31,
  by @jjedele.

## [1.0.7] - 2023-05-01 :toolbox:
- Fixes [Markdown missing a newline after simple response types](https://github.com/Neoteroi/essentials-openapi/issues/27).
- Fixes [Empty header when operations don't have any tag.](https://github.com/Neoteroi/essentials-openapi/issues/28).
- When operations don't have any tag, the `h2` element
- Improves tests.
- Adopts `pyproject.toml`.
- Workflow maintenance.

## [1.0.6] - 2023-03-19 :snail:
- Fixes a bug happening when trying to serialize examples in JSON, when they
  contain datetimes and are provided in YAML;
  ([bug report](https://github.com/Neoteroi/mkdocs-plugins/issues/35)).
- Fixes a bug related to missing resolution of references for `requestBody`;
  ([bug report](https://github.com/Neoteroi/essentials-openapi/issues/21)).
- Fixes support for code fences (disables by default `autoescape`, since the
  source of OpenAPI Specification files is supposed to be trusted anyway.
  Those who still wants to have `autoescape` enabled with `Jinja` can do so
  setting an environment variable: `SELECT_AUTOESCAPE=1`.
  ([bug report](https://github.com/Neoteroi/essentials-openapi/issues/24)).

## [1.0.5] - 2022-12-22 :santa:
- Fixes [#22](https://github.com/Neoteroi/essentials-openapi/issues/22)

## [1.0.4] - 2022-11-06 :snake:
- Fixes [#18](https://github.com/Neoteroi/essentials-openapi/issues/18)
- Workflow maintenance

## [1.0.3] - 2022-10-02
- Changes how `httpx` version is pinned (`<1`)

## [1.0.2] - 2022-05-08
- Adds support for OpenAPI specification files split into multiple files
  https://github.com/Neoteroi/mkdocs-plugins/issues/5
- Adds support for `externalDocs` and `tags` root properties

## [1.0.1] - 2022-05-05
- Adds a new output style, to provide an overview of the API endpoints with
  PlantUML
- Fixes two bugs caused by improper handling of OpenAPI Documentation without
  `components` https://github.com/Neoteroi/mkdocs-plugins/issues/9

## [1.0.0] - 2022-04-20 :sparkles:
- Adds features and a CLI to generate artifacts from OpenAPI Documentation
  files (markdown for MkDocs and PyMdown extensions, PlantUML class diagrams
  from components schemas)
- Drops support for Python 3.6

## [0.1.6] - 2021-11-17 :gem:
- Adds `py.typed` file
- Add `Python 3.10` to the GitHub Workflow

## [0.1.5] - 2021-06-27 :european_castle:
- Applies `isort` and enforces `isort` and `black` checks in CI pipeline
- Adds support for examples defined using any class declaring a `dict` callable
  method, thus including `pydantic` models
- Marks the package as `Production/Stable`

## [0.1.4] - 2021-06-19 :droplet:
- Restores support for enums on examples `@dataclasses`, after the fix
  implemented in `0.1.3`
- Adds support for built-in `UUID`, `time`, `date`, `datetime`, `bytes`,
  handling in examples for `YAML` format
- Adds `partial-time` ValueFormat for `time` (see
  https://xml2rfc.tools.ietf.org/public/rfc/html/rfc3339.html#anchor14)

## [0.1.3] - 2021-06-17 :droplet:

- Corrects a bug forcing `camelCase` on examples objects handled as dataclasses
- Adds base64 ValueFormat to the v3 enum

## [0.1.2] - 2021-05-03 :notes:

- Adds a changelog
- Adds a code of conduct
- Updates `PyYAML` dependency to version `5.4.1`
