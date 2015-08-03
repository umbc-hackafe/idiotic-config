"""webui -- mostly-automatically generate a simple web interface.

"""

import jinja2
import logging
import requests
import functools
from idiotic import dispatcher, event, items, scenes, utils
from idiotic.item import Toggle, Trigger, Number, Motor
from idiotic.scene import Scene

MODULE_NAME = "webui"

LOG = logging.getLogger("module.webui")

SECT_INCLUDE = ("include_tags",
                "exclude_tags",
                "include_items",
                "exclude_items")

include_tags = set()
exclude_tags = set()
asset_path = None

env = None

template_args = {}

def configure(config, api, assets):
    global include_tags, exclude_tags, asset_path, env, template_args

    template_args["title"] = config.get("page_title", "idiotic")
    template_args["root"] = api.path

    asset_path = assets
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(asset_path))

    api.serve(_main_js, '/main.js', content_type="text/javascript")

    traverse(api, "/", config)

    return

def traverse(api, path, tree):
    if not tree:
        return

    sections = []
    if "sections" in tree:
        sections = tree["sections"]
    else:
        sections = [{k: tree[k] for k in tree
                     if k in SECT_INCLUDE }]

    api.serve(functools.partial(_main_page, sections),
              path, content_type="text/html")

    for key, val in tree.get("subpages", {}):
        traverse(api, utils.join_url(path, key), val)

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

def _main_page(sections, *_, **__):
    args = dict(template_args)
    args["sections"] = []
    for section in sections:
        include_tags, exclude_tags, include_items, exclude_items = (
            set(section.get(n, [])) for n in SECT_INCLUDE
        )
        sect = {"item_list": []}
        sect.update({k: v for k, v in section.items()
                     if k not in SECT_INCLUDE})

        for item in sorted(list(items.all()) + list(scenes.all()), key=lambda i:i.name):
            if not _include_item(item, include_tags, exclude_tags,
                                 include_items, exclude_items):
                continue

            item_dict = {
                "desc": item.name,
                "name": utils.mangle_name(item.name),
                "show_disable": "webui.show_disable" in item.tags,
                "state": getattr(item, "state", getattr(item, "active", None)),
                "disabled": not getattr(item, "enabled", False)
            }

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
            elif isinstance(item, Scene):
                item_dict["inputs"] = [{"type": "scene"}]
            else:
                item_dict["inputs"] = []

            sect["item_list"].append(item_dict)
        args["sections"].append(dict(sect))

    return env.get_template('main.html').render(**args)

def _main_js(*_, **__):
    return env.get_template('main.js').render()

def _include_item(item, include_tags, exclude_tags, include_items, exclude_items):
    return ((not include_tags or set(item.tags) & include_tags) or
            (item.name in include_items or
             utils.mangle_name(item.name) in include_items)) and \
            (not exclude_tags or not set(item.tags) & exclude_tags) and \
            (not exclude_items or (item.name not in exclude_items and
                                   utils.mangle_name(item.name) not in exclude_items))
