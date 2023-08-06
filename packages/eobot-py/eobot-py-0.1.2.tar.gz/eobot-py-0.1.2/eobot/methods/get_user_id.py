from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoEmailError, NoPasswordOrTokenError
from ..lib.eobot_request import EobotRequest


def perform_request(config=None, request=None):
    """
    Retrieves the user id for the current user

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : int
    """
    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    if config is None or isinstance(config, str):
        config = get_config(config)
    elif not isinstance(config, EobotConfig):
        raise ValueError("Invalid config, must be a EobotConfig")

    if not config.has_email():
        raise NoEmailError()

    if not config.has_token() and not config.has_password():
        raise NoPasswordOrTokenError()

    request.set_parameter("email", config.get_email())
    request.set_parameter("password", config.get_token() if config.has_token() else config.get_password())

    result = request.perform_request()

    return int(result["userid"])
