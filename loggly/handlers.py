import logging
import logging.handlers
import socket
import traceback
import json
import pytz
from datetime import datetime
from tzlocal import get_localzone
from requests_futures.sessions import FuturesSession

session = FuturesSession()

def bg_cb(sess, resp):
    """ Don't do anything with the response """
    pass

# add utc in timestamp
def get_utc_date(local_date):
    datefrmt = datetime.strptime(str(local_date), '%Y-%m-%d %H:%M:%S,%f')
    tz = get_localzone()
    local_dt = tz.localize(datefrmt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.isoformat()

# chack data is valid json or not
def is_json(data):
    try:
        json_object = json.loads(data)
    except ValueError, e:
        return False
    return True

# convert log to Json Data if log have key value pair
def format_timestamp(log):
    jsondata = json.loads(log)
    if 'timestamp' in jsondata and jsondata['timestamp'] is not None:
        jsondata['timestamp'] = get_utc_date(jsondata['timestamp'])
    else:
        # if time stamp not present added timestamp with current utc time
        jsondata['timestamp'] = datetime.utcnow().isoformat()
    return jsondata

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
            if is_json(payload):
                payload = format_timestamp(payload)
            else:
                payload = payload
            session.post(self.url, data=payload, background_callback=bg_cb)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
            
