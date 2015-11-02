"""sms -- Receive and send SMS via Voipo

"""

import json
import time
import logging
import requests
import functools
from collections import defaultdict
from idiotic import dispatcher, event

MODULE_NAME = "sms"

log = logging.getLogger("module.sms")

host = "localhost"

class SMSReceivedEvent(event.BaseEvent):
    def __init__(self, sender, recipient, body, time):
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.body = body
        self.timestamp = time

def configure(config, api, assets):
    global host
    if "host" in config:
        host = config["host"]

    if "username" in config and "password" in config:
        pass

    api.serve(receive, '/post_sms', methods=['POST'], raw_result=True,
              no_source=True, content_type="application/json", get_data="data")

def send(recipient, body):
    pass

def receive(*args, data=None, **kwargs):
    if data:
        msg = json.loads(data.decode('UTF-8'))
        evt = SMSReceivedEvent(msg.get("Message", {}).get("From", None),
                       msg.get("Message", {}).get("To", None),
                       msg.get("Message", {}).get("Body", ""),
                       msg.get("Message", {}).get("Time", time.time()))
        dispatcher.dispatch(evt)
