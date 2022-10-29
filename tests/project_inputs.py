from types import MappingProxyType

DEFAULT_ARGS = MappingProxyType(
    {
        "project_name": "awesome-project",
        "package_name": "awesome_project",
        "project_short_description": "Project to do awesome things",
        "author_name": "John Doe",
        "author_email": "john.doe@domain.com",
        "github_username_or_org_name": "my_org",
        "python_version": "3.11",
    }
)
