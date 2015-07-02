Python Logging Loggly Handler
-----------------------------

A simple Python logging Loggly handler that can be used to send to a Loggly Gen2 https endpoint. Borrowed the extra fields concept from the graypy logging library. Check out Loggly's [Python logging documentation](https://www.loggly.com/docs/python-http/) to learn more.

## Installation
Download the repository using pip 
    
    sudo pip install loggly-python-handler

## Configuration

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

## Use Configuration in python file

    import logging
    import logging.config
    import loggly.handlers

    logging.config.fileConfig('python.conf')
    logger = logging.getLogger('myLogger')

    logger.info('Test log')


Replace
<ul>
<li><strong>TOKEN: </strong>your Loggly Customer Token</li>
</ul>
