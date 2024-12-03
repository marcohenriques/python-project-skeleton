"""Test project generation."""

from itertools import product

import pytest
from pytest_cookies.plugin import Cookies  # type: ignore

from tests.constants import DEFAULT_ARGS


# Keys for which "yes"/"no" combinations need to be generated
keys_for_combinations = ["include_docker", "include_notebooks", "include_cli", "include_docs"]

# Generate all combinations of "yes" and "no" for the selected keys
combinations = list(product(["yes", "no"], repeat=len(keys_for_combinations)))

# Generate a dictionary for each combination
generated_dicts = [
    dict(DEFAULT_ARGS, **dict(zip(keys_for_combinations, combo, strict=False)))
    for combo in combinations
]


@pytest.mark.parametrize("project_inputs", generated_dicts)
def test_bake_project(cookies: Cookies, project_inputs: dict[str, str]) -> None:
    inputs = project_inputs.copy()
    print("Using inputs:", inputs)
    result = cookies.bake(extra_context=inputs)

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == DEFAULT_ARGS["project_name"]
    assert result.project_path.is_dir()
    # TODO: assert files and folders are created as expected
