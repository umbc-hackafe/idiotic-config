from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Music Room Light",
       tags=("music_room", "light", "nyi"))

Toggle("Music Room Lamp",
       tags=("music_room", "light", "nyi"))

Toggle("Music Room Motion",
        tags=("music_room", "motion", "occupancy", "nyi"))

Toggle("Music Room Door",
       tags=("music_room", "hallway", "door", "occupancy", "nyi"))

Number("Music Room Temperature",
       bindings={"http": {"pull": "cheerilee:8081/temp"}},
       tags=("music_room", "temperature", "climate", "webui.show_sparkline"))

Number("Music Room Humidity",
       bindings={"http": {"pull": "cheerilee:8081/hum"}},
       tags=("music_room", "humidity", "climate", "webui.show_sparkline"))
