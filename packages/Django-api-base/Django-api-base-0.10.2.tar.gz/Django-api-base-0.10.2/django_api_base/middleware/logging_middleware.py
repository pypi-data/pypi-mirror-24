import sys

from django_api_base.logging_conf import Logger

logger = Logger()


class LogAllServerCalls(object):
    """
    Middleware have to be defined with __init__ and __call__ method in Django 1.10 and above
    __init__ and __call__ methods are only required in django 1.10 and above.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("========================= REQUEST START =============================")

        logger.info("URL: {0}".format(request.get_full_path()))
        logger.info("METHOD: {0}".format(request.method))
        logger.info("GET PARAMS: {0}".format(request.GET))
        logger.info("POST PARAMS: {0}".format(request.POST))
        try:
            logger.info("RAW DATA : {0}".format(request.body))
        except Exception as e:
            logger.info(e.args)

        response = self.get_response(request)

        if request.get_full_path().split('/')[1] == 'api':
            logger.info("########################## RESPONSE #############################")
            logger.info(response)

        logger.info("========================= REQUEST END ===============================")

        return response


class LogAllExceptionErrors(object):
    """
    Logs the exception error messages
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Exception):
            logger.error(sys.exc_info())
        return None
