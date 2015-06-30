from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Entertainment Room Light",
       tags=("entertainment_room", "light"))
Toggle("Entertainment Room AC",
       tags=("entertainment_room", "ac", "climate"))
Toggle("Entertainment Room - Living Room Door",
       tags=("entertainment_room", "living_room", "door", "occupancy"))

Toggle("Entertainment Room - Laundry Room Door",
       tags=("entertainment_room", "laundry_room", "door", "occupancy"))
Toggle("Entertainment Room Motion",
        tags=("entertainment_room", "motion", "occupancy"))

Number("Entertainment Room Temperature",
       tags=("entertainment_room", "temperature", "climate"))
Number("Entertainment Room Humidity",
       tags=("entertainment_room", "humidity", "climate"))
