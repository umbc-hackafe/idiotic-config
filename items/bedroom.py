from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Bedroom Light",
       tags=("bedroom", "light"))

Toggle("Bedroom Mood Light",
       tags=("bedroom", "light"))

Toggle("Bedroom Fan",
       tags=("bedroom", "fan", "climate"))

Toggle("Bedroom Motion",
        tags=("bedroom", "motion", "occupancy"))

Toggle("Bedroom Door",
        tags=("bedroom", "hallway", "door", "occupancy"))

Number("Bedroom Temperature",
       tags=("bedroom", "temperature", "climate"),

Number("Bedroom Humidity",
       tags=("bedroom", "humidity", "climate"))

Toggle("Bedroom AC",
       tags=("bedroom", "ac", "climate"))
