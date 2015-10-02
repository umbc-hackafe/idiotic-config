from idiotic.item import command, BaseItem
import functools
import wink

auth = None
w = None

MODULE_NAME = "wink"

class WinkItem(BaseItem):
    def __init__(self, name, wink_item, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.wink_item = wink_item

class WinkLight(WinkItem):
    @command
    def on(self):
        self.wink_item.turn_on()

    @command
    def off(self):
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

    for device in w.device_list():
        if device.data.get("name"):
            label = device.data.get("name")
        else:
            label = device.id
        item_type = device.device_type()

        if item_type == 'light_bulb':
            item = WinkLight(label, device, tags=(item_type,"winkhub"))

            item.on()

def bind_item(item, id=None, name=None, field=None):
    pass
