from ..lib.eobot_config import EobotConfig
from ..lib.eobot_request import EobotRequest


# noinspection PyUnusedLocal
def perform_request(config=None, request=None):
    """
    Retrieves the current values in US dollar for all supported cryptocurrencies. 1 coin equals {result} US dollar.

    :param config : Not used for this request, since this API method does not require authentication
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : dict
    """
    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    request.set_parameter("supportedcoins", "true")
    request.set_parameter("currency", "USD")

    result = request.perform_request()

    for coin in result.keys():
        result[coin]["Price"] = float(result[coin]["Price"])

    return result
