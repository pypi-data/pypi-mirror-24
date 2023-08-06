from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoUserIdError
from ..lib.eobot_request import EobotRequest
from .get_user_id import perform_request as get_user_id


def perform_request(coin, on_amount, wallet_address, config=None, request=None):
    """
    Sets the withdraw settings for `coin` to automatically withdraw to `wallet_address` when `on_amount` is reached

    :param coin : Cryptocurrency to configure
    :type coin : str

    :param on_amount : Threshold to reach for automatic withdrawal
    :type on_amount : int|float

    :param wallet_address : Wallet address to withdraw funds to
    :type wallet_address : str

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : bool
    """
    if not isinstance(coin, str):
        raise ValueError("Invalid coin, must be a str")

    coin = coin.upper()

    if not isinstance(on_amount, float) and not isinstance(on_amount, int):
        raise ValueError("Invalid on_amount, must be a float or int")

    if not isinstance(wallet_address, str):
        raise ValueError("Invalid wallet_address, must be a str")

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
        config.set_user_id(get_user_id(config=config, request=request.clone()))

    auth = config.get_authentication(False)

    request.set_parameter("id", auth.user_id)
    request.set_parameter("email", auth.email)
    request.set_parameter("password", auth.password)
    request.set_parameter("withdraw", coin)
    request.set_parameter("amount", on_amount)
    request.set_parameter("wallet", wallet_address)
    request.perform_request()

    # This API method does not return anything by which we can see whether the request was successful, so assume it was
    return True
