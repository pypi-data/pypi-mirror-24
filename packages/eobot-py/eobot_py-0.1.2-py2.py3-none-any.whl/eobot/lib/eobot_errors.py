class NoUserIdError(RuntimeError):
    """
    Raised when an API method is called that requires a user id, and no user id is set in the current config
    """
    pass


class NoEmailError(RuntimeError):
    """
    Raised when an API method is called that requires a user email address, and no email is set in the current config
    """
    pass


class NoPasswordOrTokenError(RuntimeError):
    """
    Raised when an API method is called that requires either an API token or user password, and neither is set in the
    current config
    """
    pass
