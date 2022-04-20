from urllib.parse import urlencode

from openapidocs.mk.contents import FormContentWriter


def test_form_content_writer():
    data = {"message": "Lorem ipsum"}

    writer = FormContentWriter()
    assert writer.write(data) == urlencode(data)

    assert writer.handle_content_type("x-www-form-urlencoded") is True
    assert writer.handle_content_type("application/json") is False
