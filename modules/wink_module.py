from idiotic.item import Dimmer
import functools
import logging
import wink

auth = None
w = None

MODULE_NAME = "wink"

LOG = logging.getLogger("module.wink")

def configure(config, api, assets):
    base_conf = {"base_url": "https://winkapi.quirky.com",
                 "client_id": "quirky_wink_android_app",
                 "client_secret": "e749124ad386a5a35c0ab554a4f2c045"}
    base_conf.update(config)

    global auth
    auth = wink.auth(**base_conf)

    global w
    w = wink.Wink(auth, save_auth=False)

    devices = w.device_list()
    LOG.debug("Found {} devices from wink API:".format(len(devices)))
    for device in devices:
        if device.data.get("name"):
            label = device.data.get("name")
        else:
            label = device.id

        item_type = device.device_type()
        LOG.debug("  {} is type '{}'".format(label, item_type))

        if item_type == 'light_bulb':
            LOG.debug("Adding {} as WinkLight".format(label))
            item = Dimmer(label, tags=(item_type, "winkhub"))
            item.bind_on_command(functools.partial(dimmer_command, device))
        else:
            LOG.debug("{} is an unsupported type, skipping :(".format(label))

def dimmer_command(device, evt):
    if evt.command == 'set':
        device.set_brightness(float(evt.args[0]))
    elif evt.command == 'on':
        device.turn_on()
    elif evt.command == 'off':
        device.turn_off()

def bind_item(item, id=None, name=None, field=None):
    pass
