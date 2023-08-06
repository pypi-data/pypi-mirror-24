from ..lib.eobot_config import EobotConfig
from ..lib.eobot_request import EobotRequest


# noinspection PyUnusedLocal
def perform_request(coin, config=None, request=None):
    """
    Retrieves the current value for `coin` in US dollar. 1 `coin` equals {result} US dollar

    :param coin : Cryptocurrency to retrieve value for
    :type coin : str

    :param config : Not used for this request, since this API method does not require authentication
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

    request.set_parameter("coin", coin)

    result = request.perform_request()

    return float(result[coin])
