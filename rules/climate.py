from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.item import Group
from idiotic.scene import Scene
from idiotic import instance as c

import datetime

def avg(l):
    return len(l) and sum([float(x) for x in l])/len(l)

Group("Average Temperature",
      tags=("temperature",),
      state=lambda ms: avg([m.state for m in ms if m.state]),# and (datetime.datetime.now() - m.state_history.last().time).total_seconds() < 1800]),
      members=[i for i in c.items.all() if "temperature" in i.tags and "nyi" not in i.tags],
      state_translate=float)

Group("Average Humidity",
      tags=("humidity",),
      state=lambda ms: avg([m.state for m in ms if m.state]),# and (datetime.datetime.now() - m.state_history.last().time).total_seconds() < 1800]),
      members=[i for i in c.items.all() if "humidity" in i.tags and "nyi" not in i.tags],
      state_translate=float)

# Prevent furnace from turning on and of too quickly
@bind(Command(c.items.furnace, "on"))
def stop_furnace_flop(evt):
    pass

@bind(Change(c.items.average_temperature))
@bind(Change(c.items.minimum_temperature))
@bind(Change(c.items.maximum_temperature))
def temp_change(evt):
    current = float(c.items.average_temperature.state)
    if current < float(c.items.minimum_temperature.state):
        c.items.furnace.on()
    elif current > float(c.items.maximum_temperature.state):
        c.items.furnace.off()
