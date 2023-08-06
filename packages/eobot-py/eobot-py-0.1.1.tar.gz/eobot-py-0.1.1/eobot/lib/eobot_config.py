from .eobot_errors import NoUserIdError, NoEmailError, NoPasswordOrTokenError
from .eobot_authentication import EobotWriteAuthentication, EobotReadonlyAuthentication

# used as default values in EobotConfig.configure() because None is actually a valid value and will drop current values,
# which is unwanted if named arguments are not provided
_NONE = '__none__'


class EobotConfig(object):
    """
    The EobotConfig object is used to provide user credentials to API calls, where needed.
    """

    def __init__(self):
        super(EobotConfig, self).__init__()

        self._user_id = None
        self._email = None
        self._password = None
        self._token = None

    def configure(self, user_id=_NONE, email=_NONE, password=_NONE, token=_NONE):
        """
        Configures the user credentials

        :param user_id  : (Optional) Eobot user ID to use for methods that only require that
        :param email    : (Optional) Eobot username to use for methods that perform changes
        :param password : (Optional) Eobot password to use for methods that perform changes, if the user has the API
                          configured to use password instead of tokens
        :param token    : (Optional) Eobot API token to use for methods that perform changes, if the user has the API
                          configured to use tokens instead of password

        :type user_id  : int|None
        :type email    : str|None
        :type password : str|None
        :type token    : str|None

        :returns EobotConfig : the current instance, for easy method chaining
        :rtype : EobotConfig
        """
        if user_id != _NONE:
            self.set_user_id(user_id)

        if email != _NONE:
            self.set_email(email)

        if password != _NONE:
            self.set_password(password)

        if token != _NONE:
            self.set_token(token)

        return self

    def has_user_id(self):
        """
        Returns whether a user_id is configured

        :rtype : bool
        """
        return self._user_id is not None

    def set_user_id(self, user_id):
        """
        Sets the user id

        :param user_id : user_id to configure, must be an int, can be None to clear any previous user_id
        :type user_id : int|None
        :raises ValueError : if the user_id is not an int

        :returns EobotConfig : the current instance, for easy method chaining
        :rtype : EobotConfig
        """
        if user_id is not None and not isinstance(user_id, int):
            raise ValueError("Invalid user_id, it must be an int")

        self._user_id = user_id
        return self

    def get_user_id(self):
        """
        Returns the currently configured user_id

        :rtype : int
        """
        return self._user_id

    def has_email(self):
        """
        Returns whether an email is configured

        :rtype : bool
        """
        return self._email is not None

    def set_email(self, email):
        """
        Sets the email

        :param email : email to configure, must be a str, can be None to clear any previous email
        :type email : str|None
        :raises ValueError : if the email is not a str

        :returns EobotConfig : the current instance, for easy method chaining
        :rtype : EobotConfig
        """
        if email is not None and not isinstance(email, str):
            raise ValueError("Invalid email, it must be a str")

        self._email = email
        return self

    def get_email(self):
        """
        Returns the currently configured email

        :rtype : str
        """
        return self._email

    def has_password(self):
        """
        Returns whether a password is configured

        :rtype : bool
        """
        return self._password is not None

    def set_password(self, password):
        """
        Sets the password

        :param password : password to configure, must be a str, can be None to clear any previous password
        :type password : str|None
        :raises ValueError : if the password is not a str

        :returns EobotConfig : the current instance, for easy method chaining
        :rtype : EobotConfig
        """
        if password is not None and not isinstance(password, str):
            raise ValueError("Invalid password, it must be a str")

        self._password = password
        return self

    def get_password(self):
        """
        Returns the currently configured password

        :rtype : str
        """
        return self._password

    def has_token(self):
        """
        Returns whether a token is configured

        :rtype : bool
        """
        return self._token is not None

    def set_token(self, token):
        """
        Sets the token

        :param token : token to configure, must be a str, can be None to clear any previous token
        :type token : str|None
        :raises ValueError : if the token is not a str

        :returns EobotConfig : the current instance, for easy method chaining
        :rtype : EobotConfig
        """
        if token is not None and not isinstance(token, str):
            raise ValueError("Invalid token, it must be a str")

        self._token = token
        return self

    def get_token(self):
        """
        Returns the currently configured token

        :rtype : str
        """
        return self._token

    def get_authentication(self, readonly=True):
        """
        Returns the authentication parameters needed for an API call. Readonly methods only need a user_id, write-calls
        require an email and token/password

        :param readonly : (Optional) Whether to return authentication parameters for a readonly API call or for a
                          write-call
        :type readonly  : bool
        :rtype          : EobotReadonlyAuthentication|EobotWriteAuthentication
        """
        if not self.has_user_id():
            raise NoUserIdError()

        if not readonly and not self.has_email():
            raise NoEmailError()

        if not readonly and not self.has_token() and not self.has_password():
            raise NoPasswordOrTokenError()

        if readonly:
            return EobotReadonlyAuthentication(self.get_user_id())

        if self.has_token():
            return EobotWriteAuthentication(self.get_user_id(), self.get_email(), self.get_token())

        return EobotWriteAuthentication(self.get_user_id(), self.get_email(), self.get_password())


_configs = {
    "__global": EobotConfig()
}


def get_config(name=None):
    """
    Returns an `EobotConfig` object that is used to set up user credentials for use in all API calls

    :param name : (Optional) Can be used to retrieve a particular configuration. If not provided, the global config is
                  returned
    :type name  : str
    :rtype      : EobotConfig
    """
    if name is None:
        name = "__global"

    if not isinstance(name, str):
        raise ValueError("Invalid config name, it must be a str")

    if name not in _configs.keys():
        _configs[name] = EobotConfig()

    return _configs[name]
