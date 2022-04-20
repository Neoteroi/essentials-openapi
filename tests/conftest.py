from uuid import UUID

from openapidocs.mk.v3.examples import IntegerExampleHandler, StringExampleHandler

# override the UUID example generator to return the same value, so that tests can have
# reproducible outputs for assertions
StringExampleHandler.formats["uuid"] = lambda: str(
    UUID("00000000-0000-0000-0000-000000000000")
)

IntegerExampleHandler.formats = {
    "int32": lambda: 26,
    "int64": lambda: 26,
}
