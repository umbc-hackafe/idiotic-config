from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Office Light",
       tags=("office", "light", "nyi"))

Toggle("Office Motion",
        tags=("office", "motion", "occupancy", "nyi"))

Toggle("Office Door",
       tags=("office", "hallway", "door", "occupancy", "nyi"))

Number("Office Temperature",
       tags=("office", "temperature", "climate", "nyi"))

Number("Office Humidity",
       #bindings={"http": {"pull": "dash:8081/temp"}},
       tags=("office", "humidity", "climate", "nyi"))

Toggle("Office AC",
       #bindings={"http": {"pull": "dash:8081/hum"}},
       tags=("office", "ac", "climate", "nyi"))
