from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.item import Group
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

import time

def avg(l):
    return sum(l)/len(l)

Group("Average Temperature",
      tags=("temperature",),
      state=lambda ms: avg([m.state for m in ms if m.state and (time.time() - m.history.last().time) < 1800]),
      members=[i for i in items.all() if "temperature" in i.tags and "nyi" not in i.tags])

Group("Average Humidity",
      tags=("humidity",),
      state=lambda ms: avg([m.state for m in ms if m.state and (time.time() - m.history.last().time) < 1800]),
      members=[i for i in items.all() if "humidity" in i.tags and "nyi" not in i.tags])

# Prevent furnace from turning on and of too quickly
@bind(Command(items.furnace, "on"))
def stop_furnace_flop(evt):
    pass

@bind(Change(items.average_temperature))
@bind(Change(items.minimum_temperature))
@bind(Change(items.maximum_temperature))
def temp_change(evt):
    current = items.average_temperature.state
    if current < items.minimum_temperature.state:
        items.furnace.on()
    elif current > items.maximum_temperature.state:
        items.furnace.off()
