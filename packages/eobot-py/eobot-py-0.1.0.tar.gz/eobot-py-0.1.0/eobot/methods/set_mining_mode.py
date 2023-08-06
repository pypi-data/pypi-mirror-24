from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoUserIdError
from ..lib.eobot_request import EobotRequest
import get_user_id
import get_mining_mode


def perform_request(mode, config=None, request=None):
    """
    Changes the mining mode to the cryptocurrency specified

    :param mode : Mining mode to set
    :type mode : str

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : bool
    """
    if not isinstance(mode, str):
        raise ValueError("Invalid mode, must be a str")

    mode = mode.upper()

    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    if config is None or isinstance(config, str):
        config = get_config(config)
    elif not isinstance(config, EobotConfig):
        raise ValueError("Invalid config, must be a EobotConfig")

    try:
        config.get_authentication(True)
    except NoUserIdError:
        config.set_user_id(get_user_id.perform_request(config=config, request=request.clone()))

    auth = config.get_authentication(False)

    current_mode = get_mining_mode.perform_request(config=config, request=request.clone())
    if current_mode == mode:
        return True

    request.set_parameter("id", auth.user_id)
    request.set_parameter("email", auth.email)
    request.set_parameter("password", auth.password)
    request.set_parameter("mining", mode)
    request.perform_request()

    new_mode = get_mining_mode.perform_request(config=config, request=request.clone())
    return new_mode == mode
