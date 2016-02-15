Python Logging Loggly Handler
-----------------------------

[![Build Status](https://travis-ci.org/psquickitjayant/loggly-python-handler.png?branch=master)](https://travis-ci.org/psquickitjayant/loggly-python-handler) [![Coverage Status](https://coveralls.io/repos/psquickitjayant/loggly-python-handler/badge.svg)](https://coveralls.io/r/psquickitjayant/loggly-python-handler)

A simple Python logging Loggly handler that can be used to send to a Loggly Gen2 https endpoint. Borrowed the extra fields concept from the graypy logging library. Check out Loggly's [Python logging documentation](https://www.loggly.com/docs/python-http/) to learn more.

## Installation
Download the repository using pip

    sudo pip install loggly-python-handler

## Use in python
### Configuration

Create a Configuration file python.conf and add HTTPSHandler to Configuration File.

    [handlers]
    keys=HTTPSHandler

    [handler_HTTPSHandler]
    class=loggly.handlers.HTTPSHandler
    formatter=jsonFormat
    args=('https://logs-01.loggly.com/inputs/TOKEN/tag/python','POST')

    [formatters]
    keys=jsonFormat

    [loggers]
    keys=root

    [logger_root]
    handlers=HTTPSHandler
    level=INFO

    [formatter_jsonFormat]
    format={ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}
    datefmt=

### Use Configuration in python file

    import logging
    import logging.config
    import loggly.handlers

    logging.config.fileConfig('python.conf')
    logger = logging.getLogger('myLogger')

    logger.info('Test log')

## Use in Django

### settings.py

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'json': {
                'format': '{ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'verbose',
            },
            'loggly': {
                'class': 'loggly.handlers.HTTPSHandler',
                'level': 'INFO',
                'formatter': 'json',
                'url': 'https://logs-01.loggly.com/inputs/TOKEN/tag/python',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', ],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            },
            'your_app_name': {
                'handlers': ['console', 'loggly'],
                'level': 'INFO',
            },
        },
    }

### views.py

    import logging

    logger = logging.getLogger(__name__)

    def logging_example(request):
        """logging example
        """
        logger.debug('this is DEBUG message.')
        logger.info('this is INFO message.')
        logger.warning('this is WARNING message.')
        logger.error('this is ERROR message.')
        logger.critical('this is CRITICAL message.')

        return Response({}, status=status.HTTP_200_OK)

Replace
<ul>
<li><strong>TOKEN: </strong>your Loggly Customer Token</li>
</ul>
