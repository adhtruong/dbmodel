import os
from pathlib import Path

import pytest
from mypy import api as mypy_api

CASES = [
    ("input_1.py", "output_1.txt"),
]

CONFIG_PATH = "test/mypy/pyproject.toml"

BASE_PATH = Path("test/mypy/cases")


@pytest.mark.parametrize(
    ("python_file_name", "output_file_name"),
    CASES,
)
def test_mypy_results(python_file_name: str, output_file_name: str) -> None:
    command = [
        str(BASE_PATH / python_file_name),
        "--config-file",
        CONFIG_PATH,
        "--no-incremental",
        "--cache-dir",
        f".mypy_cache/test-{os.path.splitext(python_file_name)[0]}",
    ]
    report, error, status = mypy_api.run(command)

    output_path = BASE_PATH / output_file_name
    expected_out = output_path.read_text().rstrip("\n")
    assert report.rstrip("\n") == expected_out
