from idiotic import utils

def configure(config, api, assets):
    api.serve(cmd, '/CMD', get_args="get")
    api.serve(state, "/rest/items/<item_name>/state", get_data=True,
              methods=['GET', 'POST', 'PUT'])

def cmd(get, source=None):
    if get and len({k:v for k,v in get.items() if not k.startswith('__')}) == 1:
        item = None
        cmd = None
        for k, v in get.items():
            if k.startswith('__'):
                continue
            try:
                item = items[k]
                cmd = v
                break
            except:
                continue
        else:
            raise ValueError("Arguments must contain 'item=command'")
        if hasattr(item, v):
            kwargs = {}
            if source:
                kwargs["source"] = source
            return getattr(item, v)(**kwargs)
        raise AttributeError("Item {} does not support command {}".format(item, v))
    else:
        raise ValueError("Must have exactly one 'item=command' argument")

def state(item_name, data="", source=None):
    if item_name:
        item_name = utils.mangle_name(item_name)
        try:
            item = items[item_name]
            if data:
                item._set_state_from_context(data, source=source)
                item.state = data
            return str(item.state)
        except AttributeError:
            raise AttributeError("Item {} does not exist".format(item_name))
    raise ValueError("No item specified")
