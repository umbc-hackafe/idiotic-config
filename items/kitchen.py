from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Kitchen Light",
       tags=("kitchen", "light", "nightlight"),
       bindings={"x10": {"code": "a2"}})
Toggle("Kitchen Counter Light",
       tags=("kitchen", "light"),
       bindings={"x10": {"code": "a4"}})
Toggle("Kitchen Table Light",
       tags=("kitchen", "light", "nightlight"),
       bindings={"x10": {"code": "a3"}})
Toggle("Kitchen Stove Light",
       tags=("kitchen", "light"),
       bindings={"x10": {"code": "a7"}})

Toggle("Kitchen Door",
       tags=("kitchen", "exterior_door", "occupancy", "nyi"))

Toggle("Kitchen Motion",
       tags=("kitchen", "motion", "occupancy", "nyi"))
