class MarathonError(Exception):
    pass


class MarathonHttpError(MarathonError):

    def __init__(self, response):
        """
        :param :class:`requests.Response` response: HTTP response
        """
        content = response.json()
        self.status_code = response.status_code
        self.error_message  = content['message']
        super(MarathonHttpError, self).__init__(self.__str__() )

    def __repr__(self):
        return 'MarathonHttpError: HTTP %s returned with message, "%s"' % \
               (self.status_code, self.error_message)

    def __str__(self):
        return self.__repr__()


class NotFoundError(MarathonHttpError):
    pass


class InternalServerError(MarathonHttpError):
    pass


class InvalidOperatorError(MarathonError):

    def __init__(self, operator):
        super(InvalidOperatorError, self).__init__('Invalid operator {operator}'.format(operator=operator))