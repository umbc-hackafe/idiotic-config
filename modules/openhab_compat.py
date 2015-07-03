import idiotic

def configure(config, api, assets):
    api.serve(cmd, '/CMD', get_args="get")
    api.serve(state, "/rest/items/{}/state", get_data=True)

def cmd(get, source=None):
    if get and len({k:v for k,v in get.items() if not k.startswith('__')}) == 1:
        item = None
        cmd = None
        for k, v in get.items():
            if k.startswith('__'):
                continue
            try:
                item = getattr(idiotic.items, idiotic._mangle_name(k))
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

def state(item, data="", source=None):
    if item and len(item) == 1:
        if data:
            item_name = idiotic._mangle_name(items.items()[0])
            try:
                item = getattr(idiotic.items, item_name)
                item._set_state_from_context(data, source=source)
                item.state = data
            except AttributeError:
                raise AttributeError("Item {} does not exist".format(item_name))
    return str(item.state)
