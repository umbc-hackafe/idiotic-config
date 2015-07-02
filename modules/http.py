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

def bind_item(item, actions, options={}):
    # {"<command>": ("GET", "google.com/{command}")
    if isinstance(actions, str):
        # always request same url for every command, default to GET
        item.bind_on_command(functools.partial(_binding, "GET", actions, options))
    elif isinstance(actions, dict):
        # request a different url for every command
        for command, action in actions.items():
            if isinstance(action, str):
                # default to GET
                item.bind_on_command(functools.partial(_binding, "GET", action, options), command=command)
            else:
                # specific HTTP method
                method, url = action
                item.bind_on_command(functools.partial(_binding, method, action, options), command=command)
    elif isinstance(actions, tuple) or isinstance(actions, list):
        # same url for every command, specific HTTP method
        method, url = action
        item.bind_on_command(functools.partial(_binding, method, action, options), command=command)
    else:
        raise ValueError("Invalid http binding configuration; expected dict, tuple, or str; got {}".format(type(actions)))

def _binding(method_name, url, options, event):
    method = METHODS[method_name.upper()]
    # command name, item name, and item current state will be
    # formatted into the URL by name
    method(url.format(command=str(event.command),
                      item=getattr(event.item, "name", ""),
                      state=getattr(event.item, state, None)),
           **options)
