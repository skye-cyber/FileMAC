class FilemacError(Exception):
    """Custom filemac exception handler"""

    pass


class ValidationError(FilemacError):
    """Raised when validation fails."""

    pass


class SystemPermissionError(FilemacError):
    """
    Raised when user cannot acess to system reasource due to insuficient permissions.
    Eg command execusion
    """

    pass


class FileSystemError(FilemacError):
    """
    Raises when there is file/folder ie FileSystem acess error not related to permissions.
    ie write error
    """

    pass


class AuthorizationError(FilemacError):
    """
    Raised when there is an *Explicit* file/dir/resource access denial.
        When priviledge elevelation is required.
    """

    pass


class ConfigurationError(FilemacError):
    """Raised when invalid configuration."""

    pass
