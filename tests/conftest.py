import shutil
from uuid import UUID

from essentials.folders import ensure_folder

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

try:
    shutil.rmtree("_test_files")
except OSError:
    pass

ensure_folder("_test_files")
