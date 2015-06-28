from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Office Light",
       tags=("office", "light"))

Trigger("Office Motion",
        tags=("office", "motion", "occupancy"))

Toggle("Office Door",
       tags=("office", "hallway", "door", "occupancy"))

Number("Office Temperature",
       tags=("office", "temperature", "climate"))

Number("Office Humidity",
       tags=("office", "humidity", "climate"))

Toggle("Office AC",
       tags=("office", "ac", "climate"))
