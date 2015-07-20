"""webui -- mostly-automatically generate a simple web interface.

"""

import jinja2
import logging
import requests
import functools
from idiotic import dispatcher, event, items, scenes, utils
from idiotic.item import Toggle, Trigger, Number, Motor

MODULE_NAME = "webui"

log = logging.getLogger("module.webui")

include_tags = set()
exclude_tags = set()
asset_path = None

env = None

template_args = {}

def configure(config, api, assets):
    global include_tags, exclude_tags, asset_path, env, template_args

    template_args["title"] = config.get("page_title", "idiotic")
    template_args["root"] = api.path

    include_tags = set(config.get("include_tags", []))
    exclude_tags = set(config.get("exclude_tags", []))
    include_items = set(config.get("include_items", []))
    exclude_items = set(config.get("exclude_items", []))
    asset_path = assets

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(asset_path))

    api.serve(functools.partial(_main_page, include_tags, exclude_tags,
                                include_items, exclude_items),
              '/', content_type="text/html")
    api.serve(_main_js, '/main.js', content_type="text/javascript")
    traverse(api, '/', config.get("subpages", {}))

def traverse(api, path, tree):
    if not tree:
        return

    for key, val in tree.items():
        include_tags = set(val.get("include_tags", []))
        exclude_tags = set(val.get("exclude_tags", []))
        include_items = set(val.get("include_items", []))
        exclude_items = set(val.get("exclude_items", []))

        api.serve(functools.partial(_main_page, include_tags,
                                    exclude_tags, include_items, exclude_items),
                  utils.join_url(path, key),
                  content_type="text/html")
        traverse(api, utils.join_url(path, key), val.get("subpages", {}))

def scene(name, command=None, **kwargs):
    scene = getattr(scenes, name)
    if command == "enter":
        scene.enter()
    elif command == "exit":
        scene.exit()
    elif command is not None:
        raise NameError("Command '{}' does not exist on scene {}".format(
            command, scene))
    return scene.active

def _main_page(include_tags, exclude_tags, include_items, exclude_items, *_, **__):
    args = dict(template_args)
    args["items"] = []
    for item in sorted(items.all(), key=lambda i:i.name):
        if not _include_item(item, include_tags, exclude_tags,
                             include_items, exclude_items):
            continue

        item_dict = {
            "desc": item.name,
            "name": utils.mangle_name(item.name),
            "show_disable": "webui.show_disable" in item.tags,
            "state": getattr(item, "state", None)}

        if isinstance(item, Number):
            item_dict["inputs"] = [{"command": "set",
                                    "type": "number"}]
        elif isinstance(item, Toggle):
            item_dict["inputs"] = [{"command": "on",
                                    "type": "button"},
                                   {"command": "off",
                                    "type": "button"},
                                   {"command": "toggle",
                                    "type": "button"}]
        elif isinstance(item, Trigger):
            item_dict["inputs"] = [{"command": "trigger",
                                    "type": "button"}]
        elif isinstance(item, Motor):
            item_dict["inputs"] = [{"command": "forward",
                                    "type": "button"},
                                   {"command": "reverse",
                                    "type": "button"},
                                   {"command": "stop",
                                    "type": "button"}]
        else:
            item_dict["inputs"] = []

        args["items"].append(item_dict)

    args["scenes"] = []
    for scene in sorted(scenes.all(), key=lambda i:i.name):
        scene_dict = {"desc": scene.name,
                      "name": utils.mangle_name(scene.name),
                      "active": bool(scene)
        }
        args["scenes"].append(scene_dict)

    return env.get_template('main.html').render(**args)

def _main_js(*_, **__):
    return env.get_template('main.js').render()

def _include_item(item, include_tags, exclude_tags, include_items, exclude_items):
    return ((not include_tags or set(item.tags) & include_tags) or
            (item.name in include_items)) and \
            (not exclude_tags or not set(item.tags) & exclude_tags) and \
            (not exclude_items or not item.name in exclude_items)
