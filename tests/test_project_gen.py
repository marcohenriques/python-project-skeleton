"""Test project generation."""

from pytest_cookies.plugin import Cookies  # type: ignore

from tests.constants import DEFAULT_ARGS


def test_bake_project(cookies: Cookies) -> None:
    inputs = DEFAULT_ARGS.copy()
    result = cookies.bake(extra_context=inputs)

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == DEFAULT_ARGS["project_name"]
    assert result.project_path.is_dir()
    # TODO: assert files and folders are created as expected
