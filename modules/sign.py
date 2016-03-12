"""sign -- Add and remove messages from the LED sign.

"""

import time
import asyncio
import logging
import requests
import functools
from collections import defaultdict
from idiotic import event

MODULE_NAME = "sign"

LOG = logging.getLogger("module.sign")

host = "localhost"
port = 8800
messages = []

class Message:
    def __init__(self, message, name=None, effects=[], priority=5,
                 lifetime=None, expiration=None):
        self.message = message
        self.effects = effects
        self.priority = priority
        self.lifetime = lifetime
        self.expiration = expiration
        self.name = name

    def update(self, local=False, **kwargs):
        valid = {k: v for k, v in kwargs.items() if v != None and k in (
            "message", "effects", "priority", "lifetime", "expiration"
        )}

        self.__dict__.update(valid)

        if not local:
            self.add()

        return self

    def get_expiration(self):
        if self.lifetime:
            return time.time() + self.lifetime
        elif self.expiration:
            return self.expiration
        else:
            return 2147483647 # meh

    def add(self):
        asyncio.get_event_loop().call_soon(self._add_request)

    def remove(self):
        asyncio.get_event_loop().call_soon(self._remove_request)

    def _add_request(self):
        data = {
            "text": self.message,
            "effects": ",".join(self.effects).lower(),
            "priority": self.priority,
            "expiration": int(self.get_expiration())
        }

        if self.name:
            data["name"] = self.name

        r = requests.post("http://{}:{}/add_message".format(host, port), data=data)

        r.raise_for_status()

        self.name = r.text

    def _remove_request(self):
        if self.name:
            r = requests.post("http://{}:{}/remove_message/{}".format(
                host, port, self.name))

def clear():
    # Should probably implement this on the other side
    requests.post("http://{}:{}/clear".format(host, port))

def configure(config, api, assets):
    global host, port

    if not config:
        config = {}

    host = config.get("host", "localhost")
    port = config.get("port", 8800)

def bind_item(item, commands=None, state=None):
    if commands:
        command_conf = _normalize_conf(commands)

        LOG.debug(command_conf)

        for commands, message, deletes in command_conf:
            LOG.debug("Message: {}".format(message))
            _do_command_bind(item, commands, message, deletes)

    if state:
        state_conf = _normalize_conf(state)

        for states, message, deletes in state_conf:
            _do_state_bind(item, states, message, deletes)

def new_message(*args, **kwargs):
    msg = Message(*args, **kwargs)
    msg.add()
    return msg

def _do_command_bind(item, commands, message, deletes):
    original_message = message.message
    item.bind_on_command(functools.partial(_command_bind,
                                           item, commands,
                                           message, deletes,
                                           original_message))

def _do_state_bind(item, states, message, deletes):
    original_message = message.message
    item.bind_on_change(functools.partial(_state_bind,
                                                item, states,
                                                message, deletes,
                                                original_message))

def _command_bind(item, commands, message, deletes, original_message, event):
    if not commands or event.command in commands:
        message.update(message=original_message.format(item=item, event=event))
    elif deletes and event.command in deletes:
        message.remove()

def _state_bind(item, states, message, deletes, original_message, event):
    if not states or event.new in states:
        message.update(message=original_message.format(item=item, event=event,
                                                       state=event.new))
    elif deletes and event.new in deletes:
        message.remove()

# Why do I do this to myself
def _normalize_conf(conf):
    if isinstance(conf, (str, dict)):
        return [([], _normalize_message(conf), [])]
    elif isinstance(conf, list):
        return [_normalize_conf_part(c) for c in conf]
    elif isinstance(conf, tuple):
        return [_normalize_conf_part(conf)]

def _normalize_conf_part(conf):
    try:
        try:
            cond, msg, delete = conf
            return (_normalize_condition(cond),
                    _normalize_message(msg),
                    _normalize_condition(delete))
        except ValueError:
            cond, msg = conf
            return (_normalize_condition(cond),
                    _normalize_message(msg),
                    [])
    except ValueError:
        msg = conf
        return ([], _normalize_message(msg), [])

def _normalize_condition(val):
    if isinstance(val, (list, tuple)):
        return val
    elif isinstance(val, str):
        return [val]
    else:
        return [val]

def _normalize_message(message):
    LOG.debug("normaliing {}".format(message))
    if isinstance(message, str):
        return Message(message)
    elif isinstance(message, dict):
        return Message("").update(True, **message)
    else:
        LOG.warn("Returning None: message is {}, type is {}".format(message, type(message)))
        return None
