"""x10 -- Control wired devices with the X10 protocol.

"""

import logging
import requests
import functools
from collections import defaultdict
from idiotic import dispatcher, event

MODULE_NAME = "x10"

log = logging.getLogger("module.x10")

host = "localhost"

class X10Event(event.BaseEvent):
    def __init__(self, house, unit, command):
        super().__init__()
        self.house = house
        self.unit = unit
        self.command = command

def configure(config, api, assets):
    global host
    if "host" in config:
        host = config["host"]

    api.serve(on, '/on/<house>/<unit>')
    api.serve(off, '/off/<house>/<unit>')
    api.serve(bright, '/bright/<house>/<unit>')
    api.serve(dim, '/dim/<house>/<unit>')

def bind_item(item, code=None, actions=None,
              incoming=None, outgoing=None):
    if not actions:
        actions = defaultdict(None, {"off":"off", "on":"on"})
    if not incoming:
        incoming = actions
    if not outgoing:
        outgoing = actions

    if not code:
        raise ValueError("code must be given")

    house = code[:1].lower()
    unit = code[1:]
    log.debug("binding {} to x10".format(item))
    item.bind_on_command(functools.partial(_evt_bind, outgoing.copy(), house, unit), kind="after")

def _evt_bind(cmd_dict, house, unit, event):
    _act(cmd_dict[event.command], house, unit)

def _act(act, house, unit):
    log.debug("Issuing command {}{} {}".format(house, unit, act))
    if act.lower() not in ('on', 'off', 'bright', 'dim'):
        raise ValueError("Invalid value '{}' for argument 'act'".format(act))
    if house.lower() not in "abcdefghijklmnop":
        raise ValueError("Invalid house code '{}'".format(house))
    if not 1 <= int(unit) <= 16:
        raise ValueError("Invalid unit code '{}'".format(unit))

    log.debug("Making request")

    requests.get("http://{}/{}/{}/{}".format(host, act.lower(), house.lower(), unit))

def on(house, unit):
    _act("on", house, unit)

def off(house, unit):
    _act("off", house, unit)

def bright(house, unit):
    _act("bright", house, unit)

def dim(house, unit):
    _act("dim", house, unit)
