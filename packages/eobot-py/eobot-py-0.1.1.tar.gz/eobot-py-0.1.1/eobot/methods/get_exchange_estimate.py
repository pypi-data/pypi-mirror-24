from ..lib.eobot_config import EobotConfig
from ..lib.eobot_request import EobotRequest


# noinspection PyUnusedLocal
def perform_request(from_coin, to_coin, amount, config=None, request=None):
    """
    Retrieves the estimated amount of `to_coin` you'd get for `amount` `from_coin`

    :param from_coin : Cryptocurrency to exchange from
    :type from_coin : str

    :param to_coin : Cryptocurrency to exchange to
    :type to_coin : str

    :param amount : Amount to exchange
    :type amount : float|int

    :param config : Not used for this request, since this API method does not require authentication
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : float
    """
    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    if not isinstance(from_coin, str):
        raise ValueError("Invalid from_coin, must be a str")

    if not isinstance(to_coin, str):
        raise ValueError("Invalid to_coin, must be a str")

    if not isinstance(amount, int) and not isinstance(amount, float):
        raise ValueError("Invalid amount, must be a float or int")

    from_coin = from_coin.upper()
    to_coin = to_coin.upper()

    request.set_parameter("exchangefee", "true")
    request.set_parameter("convertfrom", from_coin)
    request.set_parameter("amount", amount)
    request.set_parameter("convertto", to_coin)

    result = request.perform_request()

    return float(result["Result"])
