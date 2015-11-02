"""sms -- Receive and send SMS via Voipo

"""

import logging
import requests
import functools
from collections import defaultdict
from idiotic import dispatcher, event

MODULE_NAME = "sms"

log = logging.getLogger("module.sms")

host = "localhost"

class SMSEvent(event.BaseEvent):
    def __init__(self, sender, recipient, body):
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.body = body

def configure(config, api, assets):
    global host
    if "host" in config:
        host = config["host"]

    if "username" in config and "password" in config:
        pass

    api.serve(receive, '/post_sms', methods=['POST'], raw_result=True,
              no_source=True, content_type="application/json", get_data="json")

def send(recipient, body):
    pass

def receive(*args, json=None, **kwargs):
    log.debug(json)
