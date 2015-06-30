from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Living Room Lamp",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a6"}}
Toggle("Turtle Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a5"}})
Toggle("Living Room AC",
       tags=("living_room", "ac", "climate"))
Toggle("Front Door",
       tags=("living_room", "exterior_door", "occupancy"))
Toggle("Living Room Motion",
        tags=("living_room", "motion", "occupancy"))
Number("Living Room Temperature",
       tags=("living_room", "temperature", "climate"))
Number("Living Room Humidity",
       tags=("living_room", "humidity", "climate"))
