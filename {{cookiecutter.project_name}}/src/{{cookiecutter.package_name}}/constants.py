from enum import Enum


class StrEnum(str, Enum):
    """String enum with __str__ and __repr__ from `str`."""

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: string representation
        """
        return str.__str__(self)  # noqa: WPS609

    def __repr__(self) -> str:
        """Object representation.

        Returns:
            str: object representation
        """
        return str.__repr__(self)  # noqa: WPS609


class Environment(StrEnum):
    """Enum for app environment."""

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
