"""http -- Make HTTP(S) requests

   The MIT License (MIT)
   Copyright (c) 2015 Dylan Whichard
   http://opensource.org/licenses/MIT
"""

import logging
import requests
from idiotic import dispatcher, event, scheduler

MODULE_NAME = "http"

log = logging.getLogger("module.http")

request = requests.request
get = requests.get
post = requests.post
put = requests.put
head = requests.head
delete = requests.delete

METHODS = {
    "REQUEST": request,
    "GET": get,
    "POST": post,
    "PUT": put,
    "HEAD": head,
    "DELETE": delete
}

def configure(config, api):
    pass

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

        if isinstance(interval, int):
            scheduler.every(interval).seconds.do(call)
        elif type(interval) is scheduler.Job:
            interval.do(call)

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
            __singular_bind(item, push, tup)

    if isinstance(pull, (tuple, str)):
        __singular_bind(item, "pull", pull)
    else:
        for tup in pull:
            __singular_bind(item, "pull", pull)

def _binding(method_name, url, options, event):
    method = METHODS[method_name.upper()]
    # command name, item name, and item current state will be
    # formatted into the URL by name
    method(url.format(command=str(event.command),
                      item=getattr(event.item, "name", ""),
                      state=getattr(event.item, state, None)),
           **options)

def _schedule(item, method_name, url, options):
    method = METHODS[method_name.upper()]
    item._set_state_from_context(
        method(url.format(item=getattr(event.item, "name", ""),
                          state=getattr(event.item, state, None))),
        source="module.http")
