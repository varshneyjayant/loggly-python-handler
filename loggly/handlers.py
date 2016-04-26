import logging
import logging.handlers
import socket
import traceback
from datetime import datetime
import json
import time
import pytz
from tzlocal import get_localzone

from requests_futures.sessions import FuturesSession

session = FuturesSession()


def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass

def get_utc_date(local_date):
    datefrmt = datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S,%f')
    tz = get_localzone()
    local_dt = tz.localize(datefrmt, is_dst=None)
    return local_dt.astimezone(pytz.utc)


class HTTPSHandler(logging.Handler):
    def __init__(self, url, fqdn=False, localname=None, facility=None):
        logging.Handler.__init__(self)
        self.url = url
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            payload = self.format(record)
            jsondata = json.loads(payload)
            if jsondata['timestamp'] is not None:
                jsondata['timestamp'] =  get_utc_date(jsondata['timestamp'])
            
            session.post(self.url, data=payload, background_callback=bg_cb)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
