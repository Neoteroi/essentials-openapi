"""
Tests for template override functionality.
"""

import tempfile
from pathlib import Path

import pytest

from openapidocs.mk.generate import generate_document
from openapidocs.mk.jinja import Jinja2DocumentsWriter, OutputStyle, get_environment


def test_get_environment_with_invalid_custom_path():
    """Test that invalid custom template paths raise appropriate errors."""
    with pytest.raises(ValueError, match="does not exist"):
        get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path="/nonexistent/path",
        )


def test_get_environment_with_file_instead_of_directory():
    """Test that providing a file path instead of directory raises error."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        with pytest.raises(ValueError, match="is not a directory"):
            get_environment(
                "openapidocs.mk.v3",
                OutputStyle.MKDOCS,
                custom_templates_path=tmp_path,
            )
    finally:
        Path(tmp_path).unlink()


def test_get_environment_with_valid_custom_path():
    """Test that valid custom template path creates environment successfully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )
        assert env is not None
        assert env.loader is not None


def test_custom_template_overrides_default():
    """Test that custom template overrides the default layout.html."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom layout.html with distinctive content
        custom_template = Path(tmpdir) / "layout.html"
        custom_template.write_text("CUSTOM TEMPLATE CONTENT {{ info.title }}")

        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        # Load the template - should get our custom one
        template = env.get_template("layout.html")
        result = template.render(info={"title": "Test API"})

        assert "CUSTOM TEMPLATE CONTENT" in result
        assert "Test API" in result


def test_partial_template_override():
    """Test that individual partial templates can be overridden."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create partial subdirectory
        partial_dir = Path(tmpdir) / "partial"
        partial_dir.mkdir()

        # Override just one partial template
        custom_partial = partial_dir / "info.html"
        custom_partial.write_text("CUSTOM INFO PARTIAL")

        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        # Should load our custom partial
        template = env.get_template("partial/info.html")
        result = template.render()
        assert "CUSTOM INFO PARTIAL" in result


def test_fallback_to_default_templates():
    """Test that non-overridden templates fall back to defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create custom layout but don't override partials
        custom_template = Path(tmpdir) / "layout.html"
        custom_template.write_text("CUSTOM {{ info.title }}")

        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        # Custom template should load
        layout = env.get_template("layout.html")
        assert "CUSTOM" in layout.render(info={"title": "Test"})

        # Default partial should still be accessible
        # (this will succeed if the default partial exists)
        partial = env.get_template("partial/info.html")
        assert partial is not None


def test_jinja2_writer_with_custom_templates():
    """Test that Jinja2DocumentsWriter correctly uses custom templates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_template = Path(tmpdir) / "layout.html"
        custom_template.write_text("CUSTOM WRITER TEST")

        writer = Jinja2DocumentsWriter(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        result = writer.write({})
        assert "CUSTOM WRITER TEST" in result


def test_custom_templates_with_different_output_styles():
    """Test custom templates work with different output styles."""
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_template = Path(tmpdir) / "layout.html"
        custom_template.write_text("STYLE TEST")

        # Test with MARKDOWN style
        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MARKDOWN,
            custom_templates_path=tmpdir,
        )
        template = env.get_template("layout.html")
        assert "STYLE TEST" in template.render()

        # Test with MKDOCS style
        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )
        template = env.get_template("layout.html")
        assert "STYLE TEST" in template.render()


def test_generate_document_with_custom_templates(tmp_path):
    """Test end-to-end document generation with custom templates."""
    # Create a simple OpenAPI spec
    spec_file = tmp_path / "openapi.json"
    spec_file.write_text(
        """
{
    "openapi": "3.0.0",
    "info": {
        "title": "Test API",
        "version": "1.0.0"
    },
    "paths": {}
}
    """
    )

    # Create custom template directory
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    custom_template = templates_dir / "layout.html"
    custom_template.write_text("CUSTOM OUTPUT: {{ info.title }}")

    # Generate document with custom templates
    output_file = tmp_path / "output.md"
    generate_document(
        str(spec_file),
        str(output_file),
        style="MKDOCS",
        templates_path=str(templates_dir),
    )

    # Verify output contains custom template content
    result = output_file.read_text()
    assert "CUSTOM OUTPUT: Test API" in result


def test_generate_document_without_custom_templates(tmp_path):
    """Test that document generation works normally without custom templates."""
    spec_file = tmp_path / "openapi.json"
    spec_file.write_text(
        """
{
    "openapi": "3.0.0",
    "info": {
        "title": "Test API",
        "version": "1.0.0"
    },
    "paths": {}
}
    """
    )

    output_file = tmp_path / "output.md"
    generate_document(
        str(spec_file),
        str(output_file),
        style="MKDOCS",
        templates_path=None,
    )

    # Should generate successfully with default templates
    assert output_file.exists()
    result = output_file.read_text()
    assert "Test API" in result


def test_custom_templates_preserve_jinja_features():
    """Test that custom templates can use all Jinja2 filters and functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_template = Path(tmpdir) / "layout.html"
        # Use custom filters and functions from the environment
        custom_template.write_text(
            "{{ '/api/users/{id}' | route }} {{ read_dict(data, 'info', 'title') }}"
        )

        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        template = env.get_template("layout.html")
        result = template.render(data={"info": {"title": "My API"}})

        # Should have access to custom filters
        assert "route-param" in result or "{id}" in result
        assert "My API" in result


def test_empty_custom_templates_directory():
    """Test that an empty custom templates directory falls back to all defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Empty directory - should fall back to all defaults
        env = get_environment(
            "openapidocs.mk.v3",
            OutputStyle.MKDOCS,
            custom_templates_path=tmpdir,
        )

        # Should still be able to load default templates
        template = env.get_template("layout.html")
        assert template is not None
