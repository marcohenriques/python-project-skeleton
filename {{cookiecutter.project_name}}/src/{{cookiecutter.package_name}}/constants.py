"""Global project constants."""
from enum import Enum


class StrEnum(str, Enum):
    """String enum with __str__ and __repr__ from `str`."""

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: string representation
        """
        return str.__str__(self)

    def __repr__(self) -> str:
        """Object representation.

        Returns:
            str: object representation
        """
        return str.__repr__(self)


class Environment(StrEnum):
    """Enum for app environment."""

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
