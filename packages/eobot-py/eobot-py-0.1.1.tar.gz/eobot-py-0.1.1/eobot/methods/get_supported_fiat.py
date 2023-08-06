from ..lib.eobot_config import EobotConfig
from ..lib.eobot_request import EobotRequest


# noinspection PyUnusedLocal
def perform_request(config=None, request=None):
    """
    Retrieves the current exchange rates for all supported currencies to US dollar. 1 US dollar equals {result} currency

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

    request.set_parameter("supportedfiat", "true")

    result = request.perform_request()

    for currency in result.keys():
        result[currency]["Price"] = float(result[currency]["Price"])

    return result
