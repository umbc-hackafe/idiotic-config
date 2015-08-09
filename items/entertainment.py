from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Entertainment Room Light",
       bindings={"x10": {"code": "a13"}},
       tags=("entertainment_room", "light", "nyi"))
Toggle("Entertainment Room AC",
       tags=("entertainment_room", "ac", "climate"),
       bindings={"modlet": {"device": "noah"}})
Toggle("Entertainment Room - Living Room Door",
       tags=("entertainment_room", "living_room", "door", "occupancy", "nyi"))

Toggle("Entertainment Room - Laundry Room Door",
       tags=("entertainment_room", "laundry_room", "door", "occupancy", "nyi"))
Toggle("Entertainment Room Motion",
        tags=("entertainment_room", "motion", "occupancy", "nyi"))

Number("Entertainment Room Temperature",
       #bindings={"http": {"pull": "CHANGEME:8081/temp"}},
       tags=("entertainment_room", "temperature", "climate", "nyi"))
Number("Entertainment Room Humidity",
       #bindings={"http": {"pull": "CHANGEME:8081/hum"}},
       tags=("entertainment_room", "humidity", "climate", "nyi"))
