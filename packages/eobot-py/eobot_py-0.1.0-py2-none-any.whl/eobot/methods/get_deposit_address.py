from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoUserIdError
from ..lib.eobot_request import EobotRequest
import get_user_id


def perform_request(coin, config=None, request=None):
    """
    Retrieves the deposit wallet address for the given cryptocurrency for the current user

    :param coin : Cryptocurrency to get wallet address for
    :type coin : str

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : str
    """
    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    if not isinstance(coin, str):
        raise ValueError("Invalid coin, must be a str")

    coin = coin.upper()

    if config is None or isinstance(config, str):
        config = get_config(config)
    elif not isinstance(config, EobotConfig):
        raise ValueError("Invalid config, must be a EobotConfig")

    try:
        auth = config.get_authentication(True)
    except NoUserIdError:
        config.set_user_id(get_user_id.perform_request(config=config, request=request.clone()))
        auth = config.get_authentication(True)

    request.set_parameter("id", auth.user_id)
    request.set_parameter("deposit", coin)

    result = request.perform_request()

    return result[coin]
