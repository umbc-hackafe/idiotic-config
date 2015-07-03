from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Hallway Light",
       tags=("hallway", "light", "nightlight"),
       bindings={"x10": {"code": "b2"}})

Toggle("Hallway Motion",
        tags=("hallway", "motion", "occupancy"))

Number("Hallway Temperature",
       bindings={"http": {"pull": "scootaloo:8081/temp"}},
       tags=("hallway", "temperature", "climate"))
Number("Hallway Humidity",
       bindings={"http": {"pull": "scootaloo:8081/hum"}},
       tags=("hallway", "humidity", "climate"))
