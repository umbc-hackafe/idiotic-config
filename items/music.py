from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Music Room Light",
       tags=("music_room", "light"))

Toggle("Music Room Lamp",
       tags=("music_room", "light"))

Toggle("Music Room Motion",
        tags=("music_room", "motion", "occupancy"))

Toggle("Music Room Door",
       tags=("music_room", "hallway", "door", "occupancy"))

Number("Music Room Temperature",
       tags=("music_room", "temperature", "climate"))

Number("Music Room Humidity",
       tags=("music_room", "humidity", "climate"))
