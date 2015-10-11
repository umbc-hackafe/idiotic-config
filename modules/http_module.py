"""http -- Make HTTP(S) requests

   The MIT License (MIT)
   Copyright (c) 2015 Dylan Whichard
   http://opensource.org/licenses/MIT
"""

from aiohttp import request, get, post, put, head, delete
import logging
import asyncio
import functools
from idiotic import dispatcher, event, scheduler

MODULE_NAME = "http"

LOG = logging.getLogger("module.http")

METHODS = {
    "REQUEST": request,
    "GET": get,
    "POST": post,
    "PUT": put,
    "HEAD": head,
    "DELETE": delete
}

default_protocol = "http"

def configure(config, api, assets):
    if "default_protocol" in config:
        default_protocol = config["default_protocol"]

def __singular_bind(item, kind, tup):
    if kind == "push":
        if isinstance(tup, str):
            url = tup
            command = None
            method = "GET"
            cb = None
            options = {}
        elif len(tup) is 5:
            command, url, method, cb, options = tup
        elif len(tup) is 4:
            command, url, method, cb = tup
            options = {}
        elif len(tup) is 3:
            command, url, method = tup
            options = {}
            cb = None
        elif len(tup) is 2:
            command, url = tup
            method = "GET"
            cb = None
            options = {}
        else:
            raise ArgumentError("Invalid binding tuple for push: {}".format(tup))

        if '://' not in url:
            url = default_protocol + '://' + url

        if command == "*" or command is None:
            item.bind_on_command(functools.partial(_binding, method, url, cb, options),
                                 kind="after")
        else:
            item.bind_on_command(functools.partial(_binding, method, url, cb, options),
                                 command=command, kind="after")
    elif kind == "pull":
        if isinstance(tup, str):
            url = tup
            interval = 60
            method = "GET"
            cb = None
            options = {}
        elif len(tup) is 5:
            interval, url, method, cb, options = tup
        elif len(tup) is 4:
            interval, url, method, cb = tup
            options = {}
        elif len(tup) is 3:
            interval, url, method = tup
            cb = None
            options = {}
        elif len(tup) is 2:
            interval, url = tup
            method = "GET"
            cb = None
            options = {}
        else:
            raise ArgumentError("Invalid binding tuple for pull: {}".format(tup))

        if '://' not in url:
            url = default_protocol + '://' + url

        if isinstance(interval, int):
            scheduler.every(interval).seconds.do(_schedule, item, method, url, cb, options)
        elif type(interval) is scheduler.Job:
            interval.do(_schedule, item, method, url, cb, options)
    else:
        LOG.error("Invalid http binding type {}".format(kind))

def bind_item(item, push=[], pull=[], **kwargs):
    """Binds HTTP to an item.

    If 'method' is omitted, 'GET' is assumed.

    'url' will be formatted with keywords 'command', referring to the
    command that triggered the binding, 'item', referring to the name
    of the item, and 'state', referring to the state of the item at
    the time of the command.

    For 'push' settings, use None for all commands. <callback> will be 
    called with the request's results. For 'pull'
    settings, <frequency> may be an integral number of seconds or a
    schedule Job. <callback> will be called with the request's results,
    and should return the state to be given to the item.

    Valid forms for 'push':
    [(None|'<command>', '<url>', '<method>', <callback>, {options}), ...]
    [(None|'<command>', '<url>', '<method>', {options}), ...]
    [(None|'<command>', '<url>', '<method>'), ...]
    [(None|'<command>', '<url>'), ...]
    (None|'<command>', '<url>', '<method>', <callback>, {options})
    (None|'<command>', '<url>', '<method>', <callback>)
    (None|'<command>', '<url>', '<method>')
    (None|'<command>', '<url>')
    '<url>'

    Valid forms for 'pull':
    [(<update frequency in seconds>, '<url>', '<method>', <callback>, {options}), ...]
    [(<frequency>, '<url>', '<method>', <callback>), ...]
    [(<frequency>, '<url>', '<method>'), ...]
    [(<frequency>, '<url>'), ...]
    (<frequency>, '<url>', '<method>', <callback>, {options})
    (<frequency>, '<url>', '<method>', <callback>)
    (<frequency>, '<url>', '<method>')
    (<frequency>, '<url>')
    '<url>'

    """

    if isinstance(push, (tuple, str)):
        __singular_bind(item, "push", push)
    else:
        for tup in push:
            __singular_bind(item, "push", tup)

    if isinstance(pull, (tuple, str)):
        __singular_bind(item, "pull", pull)
    else:
        for tup in pull:
            __singular_bind(item, "pull", pull)

@asyncio.coroutine
def _binding(method_name, url, options, cb, event):
    if method_name is None:
        method_name = "GET"
    method = METHODS[method_name.upper()]

    # command name, item name, and item current state will be
    # formatted into the URL by name
    fmt_url = url.format(command=str(event.command),
               item=getattr(event.item, "name", ""),
               state=getattr(event.item, "state", None))
    res = None
    try:
        if not options:
            options = {}
        res = yield from method(fmt_url, **options)
        if res.status == 200:
            if cb:
                cb()
        else:
            LOG.warning("Request returned {} retrieving {} for item {}".format(
                res.status, fmt_url, event.item))
    except OSError:
        LOG.warning("Network error retrieving {} for item {}.".format(fmt_url, event.item))
    finally:
        if res:
            res.close()

@asyncio.coroutine
def _schedule(item, method_name, url, cb, options):
    if method_name is None:
        method_name = "GET"
    method = METHODS[method_name.upper()]
    fmt_url = url.format(item=getattr(item, "name", ""),
                         state=getattr(item, "state", None))
    res = None
    try:
        res = yield from method(fmt_url, **options)
        if res.status == 200:
            data = yield from res.read()
            text = data.decode('UTF-8')
            if cb:
                text = cb(text)
            item._set_state_from_context(text, source="module.http")
        else:
            LOG.warning("Request returned {} retrieving {} for item {}".format(
                res.status, fmt_url, item))
    except OSError:
        LOG.warning("Network error retrieving {} for item {}.".format(fmt_url, item))
    finally:
        if res:
            res.close()
