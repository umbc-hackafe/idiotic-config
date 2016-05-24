from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.item import Group, Number, display_unit
from idiotic.scene import Scene
from idiotic import instance as c

import datetime

def avg(l):
    return len(l) and sum([float(x) for x in l])/len(l)

Group("Average Temperature",
      display=display_unit("C"),
      tags=("temperature",),
      state=lambda ms: avg([m.state for m in ms if m.state]),# and (datetime.datetime.now() - m.state_history.last().time).total_seconds() < 1800]),
      members=[i for i in c.items.all() if "temperature" in i.tags and "nyi" not in i.tags],
      state_translate=float)

Group("Average Humidity",
      display=Number.DisplayWholePercent,
      tags=("humidity",),
      state=lambda ms: avg([m.state for m in ms if m.state]),# and (datetime.datetime.now() - m.state_history.last().time).total_seconds() < 1800]),
      members=[i for i in c.items.all() if "humidity" in i.tags and "nyi" not in i.tags],
      state_translate=float)
