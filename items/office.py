from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Office Light",
       bindings={"x10": {"code": "b4"}},
       tags=("office", "light"))

Toggle("Office Motion",
        tags=("office", "motion", "occupancy"))

Toggle("Office Door",
       tags=("office", "hallway", "door", "occupancy", "nyi"))

Number("Office Temperature",
       bindings={"http": {"pull": "pinkie:8081/temp"}},
       tags=("office", "temperature", "climate"))

Number("Office Humidity",
       bindings={"http": {"pull": "pinkie:8081/hum"}},
       tags=("office", "humidity", "climate"))

Toggle("Office Air Conditioner",
       tags=("office", "ac", "climate", "nyi"))
