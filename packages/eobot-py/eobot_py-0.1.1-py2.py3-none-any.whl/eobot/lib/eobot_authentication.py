class EobotReadonlyAuthentication(object):
    """
    Contains the Eobot user_id for use when authenticating against the API
    """
    def __init__(self, user_id):
        """
        :param user_id : Eobot user_id to set
        :type user_id  : int
        """
        super(EobotReadonlyAuthentication, self).__init__()
        if not isinstance(user_id, int):
            raise ValueError("Invalid user_id, must be an int")
        self.user_id = user_id


class EobotWriteAuthentication(EobotReadonlyAuthentication):
    """
    Contains the Eobot email address and password/token for use when authenticating against the API, optionally also
    includes the user_id
    """
    def __init__(self, user_id, email, password_or_token):
        """
        :param user_id           : Eobot user_id to set
        :param email             : Email address to set
        :param password_or_token : Password or token to set

        :type user_id           : int
        :type email             : str
        :type password_or_token : str
        """
        super(EobotWriteAuthentication, self).__init__(user_id)
        if not isinstance(email, str):
            raise ValueError("Invalid email, must be a str")
        self.email = email
        if not isinstance(password_or_token, str):
            raise ValueError("Invalid password_or_token, must be a str")
        self.password = password_or_token
