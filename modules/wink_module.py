from idiotic.item import command, BaseItem
import functools
import logging
import wink

auth = None
w = None

MODULE_NAME = "wink"

LOG = logging.getLogger("module.wink")

class WinkItem(BaseItem):
    def __init__(self, name, wink_item, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.wink_item = wink_item

class WinkLight(WinkItem):
    @command
    def on(self):
        LOG.debug("Turning on {}".format(self))
        self.wink_item.turn_on()

    @command
    def off(self):
        LOG.debug("Turning off {}".format(self))
        self.wink_item.turn_off()

def configure(config, api, assets):
    base_conf = {"base_url": "https://winkapi.quirky.com",
                 "client_id": "quirky_wink_android_app",
                 "client_secret": "e749124ad386a5a35c0ab554a4f2c045"}
    base_conf.update(config)

    global auth
    print(dir(wink))
    print(wink.auth)
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
            item = WinkLight(label, device, tags=(item_type,"winkhub"))
        else:
            LOG.debug("{} is an unsupported type, skipping :(".format(label))

def bind_item(item, id=None, name=None, field=None):
    pass
