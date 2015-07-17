from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Bedroom Light",
       tags=("bedroom", "light", "nyi"))

Toggle("Bedroom Mood Light",
       tags=("bedroom", "light", "nyi"))

Toggle("Bedroom Fan",
       tags=("bedroom", "fan", "climate", "nyi"))

Toggle("Bedroom AC",
       tags=("bedroom", "ac", "climate"),
       bindings={"modlet": {"device": "dylan"}})

Toggle("Bedroom Motion",
        tags=("bedroom", "motion", "occupancy", "nyi"))

Toggle("Bedroom Door",
        tags=("bedroom", "hallway", "door", "occupancy", "nyi"))

Number("Bedroom Temperature",
       bindings={"http": {"pull": "rarity:8081/temp"}},
       tags=("bedroom", "temperature", "climate"))

Number("Bedroom Humidity",
       bindings={"http": {"pull": "rarity:8081/hum"}},
       tags=("bedroom", "humidity", "climate"))
