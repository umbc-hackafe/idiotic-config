"""chromecast -- Play media on a chromecast.

"""

import logging
import functools
import mimetypes
import pychromecast
#from idiotic import name, port
name = "idiotic"
port = 80

MODULE_NAME = "chromecast"

LOG = logging.getLogger("module.chromecast")

CASTS = {}

def configure(config, api, assets):
    CASTS.update(pychromecast.get_chromecasts_as_dict())

def bind_item(item, state=None, commands=None):
    if commands:
        item.bind_on_command(functools.partial(_command_bind, commands))
        
    if state:
        item.bind_on_change(functools.partial(_state_bind, state))

def play_media(device, media, mime_type=None):
    _post_action(device, _parse_media(media), mime_type=mime_type)

def stop(device):
    cast = _find_cast(device)

    if cast:
        cast.wait()
        cast.media_controller.stop()

def _find_cast(v):
    if v in CASTS:
        return CASTS[v]

    return pychromecast.get_chromecast(friendly_name=v) or pychromecast.get_chromecast(ip=v)

def _parse_media(media, evt=None):
    if media.startswith("idiotic://"):
        media = media.replace("idiotic:///", "http://{}:{}/".format(name, port))

    return media.format(evt=evt, item=getattr(evt, "item", None))

def _post_action(device, media, mime_type=None):
    cast = _find_cast(device)

    if not mime_type:
        mime_type, _ = mimetypes.guess_type(media)

    if cast:
        cast.wait()
        cast.media_controller.play_media(media, content_type=mime_type)
    else:
        LOG.error("Unable to find chromecast '{}'".format(device))

def _command_bind(conf, evt):
    for commands, device, media in conf:
        if not commands or \
           isinstance(commands, tuple) and evt.command in commands or \
           commands == evt.command:
            _post_action(device, _parse_media(media, evt))

def _state_bind(conf, evt):
    for states, device, media,  in conf:
        if not states or \
           isinstance(states, tuple) and evt.state in states or \
           states == evt.states:
            _post_action(device, _parse_media(media, evt))
