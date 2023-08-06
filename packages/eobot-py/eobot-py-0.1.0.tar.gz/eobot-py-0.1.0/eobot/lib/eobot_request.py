from .._version import __version__
import requests


class EobotRequest(object):
    """
    Wrapper around the `requests` library to perform API requests
    """
    def __init__(self):
        super(EobotRequest, self).__init__()

        self._timeout = 30.0
        self._validate_ssl = True
        self._user_agent = 'RickDenHaan-Eobot/{0} (+http://github.com/rickdenhaan/eobot-py)'.format(__version__)
        self._base_url = 'https://www.eobot.com/api.aspx'
        self._parameters = {}

    def set_timeout(self, timeout):
        """
        Sets the request timeout

        :param timeout : timeout in seconds
        :type timeout : float|int

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(timeout, float) and not isinstance(timeout, int):
            raise ValueError("Invalid timeout, must be a float or int")

        self._timeout = float(timeout)
        return self

    def get_timeout(self):
        """
        Returns the current request timeout

        :rtype : float
        """
        return self._timeout

    def set_validate_ssl(self, validate_ssl):
        """
        Sets whether or not to validate the remote server's SSL certificate

        :param validate_ssl : whether or not to validate the certificate
        :type validate_ssl : bool

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(validate_ssl, bool):
            raise ValueError("Invalid validate_ssl, must be a bool")

        self._validate_ssl = validate_ssl
        return self

    def get_validate_ssl(self):
        """
        Returns whether or not to validate the remote server's SSL certificate

        :rtype : bool
        """
        return self._validate_ssl

    def set_user_agent(self, user_agent):
        """
        Sets the user agent for the request

        :param user_agent : user agent for the request
        :type user_agent : str

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(user_agent, str):
            raise ValueError("Invalid user_agent, must be a str")

        self._user_agent = user_agent
        return self

    def get_user_agent(self):
        """
        Returns the current user agent

        :rtype : str
        """
        return self._user_agent

    def set_base_url(self, base_url):
        """
        Sets the base URL for the request

        :param base_url : base URL for the request
        :type base_url : str

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(base_url, str):
            raise ValueError("Invalid base_url, must be a str")

        self._base_url = base_url
        return self

    def get_base_url(self):
        """
        Returns the current base URL for the request

        :rtype : str
        """
        return self._base_url

    def set_parameters(self, parameters):
        """
        Sets the request parameters

        :param parameters : request parameters
        :type parameters : dict

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(parameters, dict):
            raise ValueError("Invalid parameters, must be a dict")

        self._parameters = parameters
        return self

    def set_parameter(self, parameter, value):
        """
        Sets a specific request parameter

        :param parameter : parameter to set
        :param value : value to set for the parameter

        :type parameter : str
        :type value : str|int|float|list|dict|tuple

        :returns EobotRequest : the current instance, for easy method chaining
        :rtype : EobotRequest
        """
        if not isinstance(parameter, str):
            raise ValueError("Invalid parameter, must be a str")

        self._parameters[parameter] = value
        return self

    def get_parameters(self):
        """
        Returns the current request parameters

        :rtype : dict
        """
        return self._parameters

    def clone(self):
        """
        Creates a new request object with the same properties as this one

        :rtype : EobotRequest
        """
        clone = EobotRequest()
        clone.set_timeout(self.get_timeout())
        clone.set_validate_ssl(self.get_validate_ssl())
        clone.set_user_agent(self.get_user_agent())
        clone.set_base_url(self.get_base_url())

        return clone

    def perform_request(self):
        """
        Performs the API request and returns the response value

        :rtype : dict
        """
        url = self.get_base_url()
        headers = {
            "User-Agent": self.get_user_agent()
        }

        parameters = self.get_parameters()
        parameters["json"] = "true"

        response = requests.get(
            url,
            params=parameters,
            headers=headers,
            timeout=self.get_timeout(),
            verify=self.get_validate_ssl()
        )

        try:
            return response.json()
        except:
            raise RuntimeError("Unexpected non-JSON response: {0}".format(response.text))
