"""Integration tests configuration file for pytest."""

from pathlib import Path

import pytest


@pytest.fixture
def content_file(tmp_path: Path) -> Path:
    directory = tmp_path / "my_folder"
    directory.mkdir()
    path = directory / "my_file.txt"
    path.write_text("my content")
    return path
