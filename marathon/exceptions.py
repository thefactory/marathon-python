class MarathonError(Exception):
    pass


class MarathonHttpError(MarathonError):

    def __init__(self, response):
        """
        :param :class:`requests.Response` response: HTTP response
        """
        self.error_message = response.reason or ''
        if response.content and 'application/json' in response.headers.get('content-type', ''):
            content = response.json()
            self.error_message = content.get('message', self.error_message)
            self.error_details = content.get('details')
        self.status_code = response.status_code
        super().__init__(self.__str__())

    def __repr__(self):
        return 'MarathonHttpError: HTTP %s returned with message, "%s"' % \
               (self.status_code, self.error_message)

    def __str__(self):
        return self.__repr__()


class NotFoundError(MarathonHttpError):
    pass


class InternalServerError(MarathonHttpError):
    pass


class ConflictError(MarathonHttpError):
    pass


class InvalidChoiceError(MarathonError):

    def __init__(self, param, value, options):
        super().__init__(
            'Invalid choice "{value}" for param "{param}". Must be one of {options}'.format(
                param=param, value=value, options=options
            )
        )


class NoResponseError(MarathonError):
    pass
