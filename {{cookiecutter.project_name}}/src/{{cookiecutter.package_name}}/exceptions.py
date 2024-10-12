"""App custom exceptions."""


class {{ cookiecutter.package_name.split('_') | map('title') | join('') }}Error(Exception):
    """General error message for {{ cookiecutter.package_name }}."""
