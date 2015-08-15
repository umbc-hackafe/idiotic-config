"""modloet -- Control devices from mymodlet.com

"""

import json
import logging
import requests
import functools

MODULE_NAME = "modlet"

# If we're setting the modlet on without thermostat mode, set it to
# this so that it won't turn itself off.
LOW_TEMP = 50

LOG = logging.getLogger("module.modlet")

__user = ""
__password = ""
__cookies = {}
device_table = {}
default_poll = 60
units = "C"

def configure(config, api, assets):
    global __user, __password, default_poll, units

    __user = config.get("user", "")
    __password = config.get("password", "")

    default_poll = config.get("interval", default_poll)
    units = config.get("units", units).upper()[:1]

    devices = config.get("devices", {})
    for name, id in devices.items():
        device_table[name] = {
            "id": id,
            "temperature_item": None,
            "thermostat_items": [],
            "control_items": [],
        }

    if units not in ("F", "C", "K", "R"):
        pass

def bind_item(item, modlet=None, control=False, thermostat=False,
              temperature=False, actions=None):
    """Bind an item to control or receive data from a modlet.

    modlet:      The name of a pre-configured modlet, or a modlet ID
    control:     True if the item should control the specified modlet
    thermostat:  True if the item should receive state updates from the
                 modlet's thermostat (Not yet implemented)
    temperature: True if the item's state should control the modlet's
                 set temperature
    actions:     A dictionary of command names to "on" or "off" reflcting
                 which commands will cause the modlet to turn on or off.
                 Has no effect unless 'control' is True. Defaults to
                 linking 'on' and 'off'
    interval:    The time interval at which to poll the modlet. Overrides
                 the global config value.

    """

    modlet = device_table.get(modlet, {"id": modlet})

    if not modlet.get("id"):
        raise ValueError("A valid modlet name or ID must be specified.")

    if control:
        if not actions:
            actions = defaultdict(None, {"off":"off", "on":"on"})

        # TODO: Also support issuing commands when the modlet receives
        # a command externally
        item.bind_on_command(functools.partial(_control_bind, actions.copy(),
                                               modlet), kind="after")

    if thermostat:
        # TODO implement me
        pass

    if temperature:
        modlet["temperature_item"] = item

def _control_bind(cmd_dict, modlet, event):
    if event.command in cmd_dict:
        action = cmd_dict[event.command]
        if action == "on":
            _modlet_set(modlet, True)
        elif action == "off":
            _modlet_set(modlet, False)

def _login():
    res = requests.post("https://mymodlet.com/Account/Login",
                        data={"loginForm.Email": __user,
                              "loginForm.Password": __password,
                              "loginForm.RememberMe": "True"})

    res.raise_for_status()

    if "ASPXAUTH" in res.cookies:
        __cookies.update(res.cookies)
    else:
        raise ValueError("Invalid username or password for mymodlet.com")

def _modlet_set(modlet, val):
    set_temp = LOW_TEMP

    item = modlet.get("temperature_item")
    if item and hasattr(item, "state"):
        set_temp = to_modlet(float(item.state))

    res = requests.post("https://mymodlet.com/SmartAC/UserSettings",
                        json={"applianceId": modlet["id"],
                              "thermostated": val,
                              "targetTemperature": set_temp},
                        cookies=__cookies)

    res.raise_for_status()

    try:
        if not res.json()["Success"]:
            raise IOError("Setting modlet state failed")
    except ValueError as e:
        LOG.info("Results: {}".format(res.text))
        raise IOError("Setting modlet state failed") from e

def from_c(c, unit=units):
    if unit == "C":
        return c
    elif unit == "F":
        return c * (9 / 5) + 32
    elif unit == "K":
        return c + 273.15
    elif unit == "R":
        return (c + 273.15) * (9 / 5)
    else:
        raise NotImplementedError("Temperature units {} not supported".format(units))

def to_c(temp, unit=units):
    f=k=r=c=temp
    if unit == "C":
        return c
    elif unit == "F":
        return (f - 32) * (5 / 9)
    elif unit == "K":
        return k - 273.15
    elif unit == "R":
        return (r - 491.67) * (5 / 9)
    else:
        raise NotImplementedError("Temperature units {} not supported".format(units))

# Convert temperature into C from modlet's f, then into local units
def from_modlet(temp):
    return from_c(to_c(temp, "F"))

# Convert local temperature to C, then into F for modlet
def to_modlet(temp):
    return from_c(to_c(temp), "F")

