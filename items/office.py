from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Office Light",
       tags=("office", "light"))

Toggle("Office Motion",
        tags=("office", "motion", "occupancy"))

Toggle("Office Door",
       tags=("office", "hallway", "door", "occupancy"))

Number("Office Temperature",
       tags=("office", "temperature", "climate"))

Number("Office Humidity",
       #bindings={"http": {"pull": "dash:8081/temp"}},
       tags=("office", "humidity", "climate"))

Toggle("Office AC",
       #bindings={"http": {"pull": "dash:8081/hum"}},
       tags=("office", "ac", "climate"))
