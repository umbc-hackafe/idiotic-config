"""http -- Make HTTP(S) requests

   The MIT License (MIT)
   Copyright (c) 2015 Dylan Whichard
   http://opensource.org/licenses/MIT
"""

import aiohttp
import logging
import asyncio
import functools
from idiotic import dispatcher, event, scheduler

MODULE_NAME = "http"

log = logging.getLogger("module.http")

@asyncio.coroutine
def request(method, url, **kwargs):
    res = yield from aiohttp.request(method, url)
    return res

get = functools.partial(request, "GET")
post = functools.partial(request, "POST")
put = functools.partial(request, "PUT")
post = functools.partial(request, "POST")
head = functools.partial(request, "HEAD")
delete = functools.partial(request, "DELETE")

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
            options = {}
        elif len(tup) is 4:
            command, url, method, options = tup
        elif len(tup) is 3:
            command, url, method = tup
            options = {}
        elif len(tup) is 2:
            command, url = tup
            method = "GET"
            options = {}
        else:
            raise ArgumentError("Invalid binding tuple for push: {}".format(tup))

        if '://' not in url:
            url = default_protocol + '://' + url

        if command == "*" or command is None:
            item.bind_on_command(lambda e: _binding(method, url, options, e))
        else:
            item.bind_on_command(lambda e: _binding(method, url, options, e), command=command)
    elif kind == "pull":
        if isinstance(tup, str):
            url = tup
            interval = 60
            method = "GET"
            options = {}
        elif len(tup) is 4:
            interval, url, method, options = tup
        elif len(tup) is 3:
            interval, url, method = tup
            options = {}
        elif len(tup) is 2:
            interval, url = tup
            method = "GET"
            options = {}
        else:
            raise ArgumentError("Invalid binding tuple for pull: {}".format(tup))

        call = lambda: _schedule(item, method, url, options)

        if '://' not in url:
            url = default_protocol + '://' + url

        if isinstance(interval, int):
            scheduler.every(interval).seconds.do(call)
        elif type(interval) is scheduler.Job:
            interval.do(call)
    else:
        log.error("Invalid http binding type {}".format(kind))

def bind_item(item, push=[], pull=[], **kwargs):
    """Binds HTTP to an item.

    If 'method' is omitted, 'GET' is assumed.

    'url' will be formatted with keywords 'command', referring to the
    command that triggered the binding, 'item', referring to the name
    of the item, and 'state', referring to the state of the item at
    the time of the command.

    For 'push' settings, use None for all commands. For 'pull'
    settings, <frequency> may be an integral number of seconds or a
    schedule Job.

    Valid forms for 'push':
    [(None|'<command>', '<url>', '<method>'), ...]
    [(None|'<command>', '<url>'), ...]
    (None|'<command>', '<url>', '<method>')
    (None|'<command>', '<url>')
    '<url>'

    Valid forms for 'pull':
    [(<update frequency in seconds>, '<url>', '<method>'), ...]
    [(<frequency>, '<url>'), ...]
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

def _binding(method_name, url, options, event):
    method = METHODS[method_name.upper()]
    # command name, item name, and item current state will be
    # formatted into the URL by name
    fmt_url = url.format(command=str(event.command),
               item=getattr(event.item, "name", ""),
               state=getattr(event.item, "state", None))
    try:
        res = yield from method(fmt_url, **options)
        if res.status != 200:
            log.warning("Request returned {} retrieving {} for item {}".format(
                res.status, fmt_url, event.item))
    except OSError:
        log.warning("Network error retrieving {} for item {}.".format(fmt_url, event.item))

def _schedule(item, method_name, url, options):
    method = METHODS[method_name.upper()]
    fmt_url = url.format(item=getattr(item, "name", ""),
                         state=getattr(item, "state", None))
    try:
        res = yield from method(fmt_url, **options)
        if res.status == 200:
            text = yield from res.read()
            item._set_state_from_context(text, source="module.http")
        else:
            log.warning("Request returned {} retrieving {} for item {}".format(
                res.status, fmt_url, item))
    except OSError:
        log.warning("Network error retrieving {} for item {}.".format(fmt_url, item))
