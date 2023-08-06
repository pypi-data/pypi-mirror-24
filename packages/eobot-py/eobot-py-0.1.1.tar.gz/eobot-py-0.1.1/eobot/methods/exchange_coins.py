from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoUserIdError
from ..lib.eobot_request import EobotRequest
from .get_balances import perform_request as get_balances
from .get_user_id import perform_request as get_user_id


def perform_request(from_coin, amount, to_coin, config=None, request=None):
    """
    Exchanges `amount` `from_coin` to `to_coin` (note: Eobot will withhold a percentage as fee when doing this)

    :param from_coin : Cryptocurrency to exchange from
    :type from_coin : str

    :param amount : Amount to exchange
    :type amount : int|float

    :param to_coin : Cryptocurrency to exchange to
    :type to_coin : str

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : bool
    """
    if not isinstance(from_coin, str):
        raise ValueError("Invalid from_coin, must be a str")

    from_coin = from_coin.upper()

    if not isinstance(amount, float) and not isinstance(amount, int):
        raise ValueError("Invalid amount, must be a float or int")

    if not isinstance(to_coin, str):
        raise ValueError("Invalid to_coin, must be a str")

    to_coin = to_coin.upper()

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

    old_balances = get_balances(config=config, request=request.clone())
    old_balance_from = old_balances[from_coin] if from_coin in old_balances.keys() else 0.0
    old_balance_to = old_balances[to_coin] if to_coin in old_balances.keys() else 0.0

    request.set_parameter("id", auth.user_id)
    request.set_parameter("email", auth.email)
    request.set_parameter("password", auth.password)
    request.set_parameter("convertfrom", from_coin)
    request.set_parameter("amount", amount)
    request.set_parameter("convertto", to_coin)
    request.perform_request()

    new_balances = get_balances(config=config, request=request.clone())
    new_balance_from = new_balances[from_coin] if from_coin in new_balances.keys() else 0.0
    new_balance_to = new_balances[to_coin] if to_coin in new_balances.keys() else 0.0

    return new_balance_from < old_balance_from and new_balance_to > old_balance_to
