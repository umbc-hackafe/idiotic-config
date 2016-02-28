"""webui -- mostly-automatically generate a simple web interface.

"""

import jinja2
import logging
import datetime
import requests
import functools
from flask import Response, request
from idiotic import dispatcher, event, items, scenes, utils
from idiotic.item import Toggle, Trigger, Number, Motor, Text
from idiotic.scene import Scene

MODULE_NAME = "webui"

LOG = logging.getLogger("module.webui")

USE_GRAPHS = False

try:
    import pygal
    USE_GRAPHS = True
except:
    LOG.warning("Could not import pygal; graphs are disabled")

SECT_INCLUDE = ("include_tags",
                "exclude_tags",
                "include_items",
                "exclude_items")

include_tags = set()
exclude_tags = set()
default_graph = False
asset_path = None

env = None

template_args = {}

def configure(config, api, assets):
    global include_tags, exclude_tags, asset_path, env, template_args
    global default_graph

    template_args["title"] = config.get("page_title", "idiotic")
    template_args["root"] = api.path

    default_graph = config.get("enable_graph", False)

    asset_path = assets
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(asset_path))

    api.add_url_rule('/main.js', '_main_js', _main_js)
    api.add_url_rule('/sparkline/<item>.svg', '_sparkline', _sparkline)
    api.add_url_rule('/graph/<item>.svg', '_graph', _graph)

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

    api.add_url_rule(path, path.replace('/', '_'), functools.partial(_main_page, sections))

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
                "show_sparkline": "webui.show_sparkline" in item.tags,
                "enable_graph": default_graph,
                "state": getattr(item, "state", getattr(item, "active", None)),
                "disabled": not getattr(item, "enabled", False)
            }

            if "webui.enable_graph" in item.tags:
                item_dict["enable_graph"] = True
            elif "webui.disable_graph" in item.tags:
                item_dict["enable_graph"] = False

            if isinstance(item, Number):
                item_dict["inputs"] = [{"command": "set",
                                        "type": "number"}]
            elif isinstance(item, Text):
                item_dict["inputs"] = [{"command": "set",
                                        "type": "text"}]
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

    return Response(env.get_template('main.html').render(**args), mimetype='text/html')

def _main_js(*_, **__):
    return Response(env.get_template('main.js').render(), mimetype='text/javascript')

def __empty_svg():
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <svg
xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1 1"
width="1" height="1" id="svg_pixel"> </svg>"""

def _sparkline(item, *args, **kwargs):
    if USE_GRAPHS:
        history = items[item].state_history
        if not history:
            return __empty_svg()

        _, values = zip(*history.last(min(10, len(history))))

        graph = pygal.Line(interpolate='cubic', style=pygal.style.LightStyle)
        graph.add("Last 10", values)
        return Response(graph.render_sparkline(height=25).decode('UTF-8'), mimetype='image/svg+xml')
    else:
        return Response(__empty_svg(), mimetype='image/svg+xml')

def __avg_time(datetimes):
    total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in datetimes)
    avg = total / len(datetimes)
    minutes, seconds = divmod(int(avg), 60)
    hours, minutes = divmod(minutes, 60)
    return datetime.datetime.combine(datetime.date(1900, 1, 1), datetime.time(hours, minutes, seconds))

def __group(times, values, count=50, group=lambda v: sum(v)/len(v)):
    if len(times) != len(values):
        raise ValueError("times and values must have same length")

    if len(times) < count or len(times) < 2:
        return times, values

    count = min(count, len(times))

    diff = (times[-1] - times[0]) / count

    divisions = [times[0] + i * diff for i in range(count)] + [times[-1]]

    temp = []

    res = []

    partitions = zip(divisions[0:], divisions[1:])

    i = 0
    for start, end in partitions:
        while i < len(times) and start <= times[i] <= end:
            temp.append((times[i], values[i]))
            i += 1
        else:
            if temp:
                ts, vs = zip(*temp)
                res.append((__avg_time(ts), group(vs)))
            temp = []

    return zip(*res)

def _graph(item, *_, **kwargs):
    args = utils.single_args(request.args)

    time = args.get('time', 86400)
    offset = args.get('offset', 0)
    count = args.get('count', None)

    if USE_GRAPHS:
        history = items[item].state_history
        if not history:
            return Response(__empty_svg(), mimetype='image/svg+xml')

        if count:
            times, values = zip(*history.last(min(10, len(history))))
        else:
            times, values = zip(*history.since(datetime.datetime.now() - datetime.timedelta(seconds=int(time))))

        times, values = __group(times, values)

        graph = pygal.Line(style=pygal.style.LightStyle, x_label_rotation=-60)
        graph.title = items[item].name
        graph.add("Value", values)
        graph.x_labels = (t.strftime("%H:%M:%S") for t in times)
        return Response(graph.render().decode('UTF-8'), mimetype='image/svg+xml')
    else:
        return Response(__empty_svg(), mimetype='image/svg+xml')

def _include_item(item, include_tags, exclude_tags, include_items, exclude_items):
    return ((not include_tags or set(item.tags) & include_tags) or
            (item.name in include_items or
             utils.mangle_name(item.name) in include_items)) and \
            (not exclude_tags or not set(item.tags) & exclude_tags) and \
            (not exclude_items or (item.name not in exclude_items and
                                   utils.mangle_name(item.name) not in exclude_items))
