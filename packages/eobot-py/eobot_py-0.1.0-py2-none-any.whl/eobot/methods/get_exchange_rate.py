from ..lib.eobot_config import EobotConfig
from ..lib.eobot_request import EobotRequest


# noinspection PyUnusedLocal
def perform_request(currency, config=None, request=None):
    """
    Retrieves the current exchange rate from `currency` to US dollar. 1 US dollar equals {result} `currency`

    :param currency : Currency to retrieve exchange rate for
    :type currency : str

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

    if not isinstance(currency, str):
        raise ValueError("Invalid currency, must be a str")

    currency = currency.upper()

    request.set_parameter("coin", currency)

    result = request.perform_request()

    return float(result[currency])
