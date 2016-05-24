from idiotic.rule import bind, Command
from idiotic.modutils import require_rules, require_items
from idiotic import instance as c
import functools

require_items('bedroom')

@bind(Command(c.items.bedroom_light, time="before"))
def do_a_thing(evt):
    print(evt)
    if evt.command == "on" and evt.item.state:
        evt.cancel()

    elif evt.command == "off" and not evt.item.state:
        evt.cancel()

    print(evt.canceled)
