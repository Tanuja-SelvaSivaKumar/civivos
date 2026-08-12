import os
from pathlib import Path


TEST_DB_PATH = (
    Path(".pytest_cache")
    / "civivos_test.db"
)

TEST_DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

os.environ["CIVIVOS_DB_PATH"] = str(
    TEST_DB_PATH
)