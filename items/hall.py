from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Hallway Light",
       tags=("hallway", "light"),
       bindings={"x10": {"code": "b2"}})

Trigger("Hallway Motion",
        tags=("hallway", "motion", "occupancy"))

Number("Hallway Temperature",
       tags=("hallway", "temperature", "climate"))
Number("Hallway Humidity",
       tags=("hallway", "humidity", "climate"))
