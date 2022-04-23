from pathlib import Path
from uuid import uuid4

import httpx
import pytest
import yaml
from click.testing import CliRunner

from openapidocs.commands.docs import generate_documents_command
from openapidocs.main import main
from openapidocs.mk.jinja import OutputStyle
from openapidocs.utils.source import SourceError, read_from_source, read_from_url
from openapidocs.utils.web import FailedRequestError, ensure_success, http_get
from tests.common import get_file_json

from .serverfixtures import *  # noqa
from .serverfixtures import BASE_URL


@pytest.fixture(scope="module")
def example_1_data():
    return get_file_json("example1-openapi.json")


def read_file(file_path):
    with open(file_path, mode="rt", encoding="utf8") as source:
        return source.read()


def remove_file(file_path: Path):
    try:
        file_path.unlink()
    except FileNotFoundError:
        return


def contents_equals(file_path_1, file_path_2):
    assert read_file(file_path_1) == read_file(file_path_2)


def test_fetch_json(example_1_data):
    response = http_get(f"{BASE_URL}/example1-openapi.json")
    data = response.json()

    assert data == example_1_data


def test_fetch_yaml(example_1_data):
    response = http_get(f"{BASE_URL}/example1-openapi.yaml")
    raw_data = response.text
    data = yaml.safe_load(raw_data)

    assert data == example_1_data


def test_failed_request():
    with pytest.raises(FailedRequestError) as failed_request:
        response = http_get(f"{BASE_URL}/missing-file.json")
        ensure_success(response)

    error = failed_request.value
    # there is no inner exception in this case
    assert error.inner_exception is None


def test_failed_request_wrong_url():
    with pytest.raises(FailedRequestError) as failed_request:
        http_get("http://localhost:80555/missing-file.json")

    error = failed_request.value
    # there is no inner exception in this case
    assert error.inner_exception is not None
    assert error.inner_exception is error.__context__
    assert isinstance(error.inner_exception, httpx.HTTPError)


def test_generate_docs_command_from_url():
    test_output = Path("test_write1.md")
    remove_file(test_output)

    runner = CliRunner()
    result = runner.invoke(
        generate_documents_command,
        ["-s", f"{BASE_URL}/example1-openapi.json", "-d", str(test_output)],
    )
    assert result.exit_code == 0
    assert test_output.exists()
    remove_file(test_output)


def test_generate_docs_command_invalid_source():
    runner = CliRunner()
    result = runner.invoke(
        generate_documents_command,
        ["-s", "...", "-d", "foo.md"],
    )
    assert result.exit_code == 2


@pytest.mark.parametrize(
    "valid_source",
    [
        f"{BASE_URL}/example1-openapi.json",
        f"{BASE_URL}/example1-openapi.yaml",
        "tests/res/example1-openapi.json",
        "tests/res/example1-openapi.yaml",
    ],
)
def test_main_command_gen_mkdocs_docs(valid_source):
    test_output = Path(f"{uuid4()}.md")
    assert test_output.exists() is False

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["gen-docs", "-s", valid_source, "-d", str(test_output)],
    )
    assert result.exit_code == 0
    assert test_output.exists()
    contents_equals(test_output, "tests/res/example1-output.md")
    remove_file(test_output)


@pytest.mark.parametrize(
    "valid_source",
    [
        f"{BASE_URL}/example1-openapi.json",
        f"{BASE_URL}/example1-openapi.yaml",
        "tests/res/example1-openapi.json",
        "tests/res/example1-openapi.yaml",
    ],
)
def test_main_command_gen_plantuml_schema_docs(valid_source):
    test_output = Path(f"{uuid4()}.wsd")
    assert test_output.exists() is False

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "gen-docs",
            "-s",
            valid_source,
            "-d",
            str(test_output),
            "-t",
            "PLANTUML_SCHEMAS",
        ],
    )
    assert result.exit_code == 0
    assert test_output.exists()
    contents_equals(test_output, "tests/res/example1-schemas-output.wsd")
    remove_file(test_output)


@pytest.mark.parametrize(
    "valid_source",
    [
        "tests/res/example1-openapi.yaml",
    ],
)
def test_main_command_gen_plantuml_api_docs(valid_source):
    test_output = Path(f"{uuid4()}.wsd")
    assert test_output.exists() is False

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "gen-docs",
            "-s",
            valid_source,
            "-d",
            str(test_output),
            "-t",
            "PLANTUML_API",
        ],
    )
    assert result.exit_code == 0
    assert test_output.exists()
    contents_equals(test_output, "tests/res/example1-api-output.wsd")
    remove_file(test_output)


def test_main_command_gen_plain_markdown_docs():
    valid_source = "tests/res/example1-openapi.json"
    test_output = Path(f"{uuid4()}.md")
    assert test_output.exists() is False

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "gen-docs",
            "-s",
            valid_source,
            "-d",
            str(test_output),
            "-t",
            "MARKDOWN",
        ],
    )
    assert result.exit_code == 0
    assert test_output.exists()

    contents_equals(test_output, "tests/res/example1-output-plain.md")
    remove_file(test_output)


def test_main_command_list_styles():
    runner = CliRunner()
    result = runner.invoke(main, ["list-styles"])
    assert result.exit_code == 0

    for value in OutputStyle:
        assert f"{value.name}: {value.value}" in result.stdout


def test_read_from_url_invalid_source():
    with pytest.raises(SourceError) as error:
        read_from_url(f"{BASE_URL}/example1-output.md")

    assert error.value is not None


def test_read_from_source_invalid_source():
    with pytest.raises(ValueError) as error:
        read_from_source("tests")

    assert str(error.value) == "The given path is not a file path."

    with pytest.raises(ValueError) as error:
        read_from_source("tests/res/example1-output.md")

    assert str(error.value) == "Unsupported source file."
