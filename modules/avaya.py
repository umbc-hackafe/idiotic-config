"""avaya -- Configure Avaya switches

"""

import logging
import requests
import functools
from collections import defaultdict

MODULE_NAME = "avaya"

LOG = logging.getLogger("module.avaya")

STATUS_COMMANDS = {
    True: "1",
    False: "2"
}

def bind_item(item, port, actions=None):
    """Bind an item to control a PoE port.

    port:        The port number to control
    """

    item.bind_on_command
    modlet = device_table.get(device, {"id": device})

    if not modlet.get("id"):
        raise ValueError("A valid modlet name or ID must be specified.")

    if not actions:
        actions = defaultdict(None, {"off":"off", "on":"on"})

        item.bind_on_command(functools.partial(_control_bind, actions.copy(),
                                               port), kind="after")

def _control_bind(cmd_dict, port, event):
    if event.command in cmd_dict:
        action = cmd_dict[event.command]
        if action == "on":
            _poe_set(port, True)
        elif action == "off":
            _poe_set(port, False)

def _poe_set(port, val):
    res = requests.post(
        "http://erika/jsp/setFormMibs.jsp",
        data={
            "command": "setVariables",
            "varNames": "pethPsePortAdminEnable.1.{}".format(port),
            "varValues": STATUS_COMMANDS[val],
            "varCount": 1,
            "timeout": 30000,
        }
    )

    res.raise_for_status()
