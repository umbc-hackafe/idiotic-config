"""modlet -- Controls modlets from mymodlet.com

   The MIT License (MIT)
   Copyright (c) 2015 Dylan Whichard
   http://opensource.org/licenses/MIT
"""

import logging
import subprocess
import functools
from idiotic import dispatcher, event, scheduler

MODULE_NAME = "modlet"

log = logging.getLogger("module.modlet")

def bind_item(item, device, **kwargs):
    item.bind_on_command(functools.partial(binding, device), kind="after")

def binding(device, evt):
    if evt.command in ("on", "off"):
        subprocess.Popen(["/usr/bin/air", device, "set", evt.command, "temp", "73"])
