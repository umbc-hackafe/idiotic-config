from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Outside Side Light",
       tags=("outside", "light", "nightlight"),
       bindings={"x10": {"code": "a8"}})
Toggle("Outside Front Light",
       tags=("outside", "light", "nightlight"),
       bindings={"x10": {"code": "a9"})
