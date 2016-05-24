from idiotic.item import Toggle, Trigger, Number, Group, Dimmer, display_unit
from idiotic import instance as c

Toggle("Music Room Light",
       tags=("music_room", "light", "nyi"))

Dimmer("Music Room Lamp",
       bindings={"wink": {"name": "Sasha Floor Lamp"}},
       tags=("music_room", "light"))

Trigger("Music Room Motion",
        tags=("music_room", "motion", "occupancy", "nyi"))

Toggle("Music Room Door",
       display=Toggle.DisplayOpenClosed,
       tags=("music_room", "hallway", "door", "occupancy", "nyi"))

Number("Music Room Temperature",
       display=display_unit("C"),
       bindings={"http": {"pull": "cheerilee:8081/temp"}},
       tags=("music_room", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))

Number("Music Room Humidity",
       display=Number.DisplayWholePercent,
       bindings={"http": {"pull": "cheerilee:8081/hum"}},
       tags=("music_room", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))

Toggle("Music Room Air Conditioner",
       tags=("music_room", "ac", "climate", "nyi"))

c.modules.thermostat.Thermostat(
    "Music Room Thermostat",
    display=display_unit("C"),
    tags=("webui.show_disable", "heat", "nyi"),
    chillers=[c.items.music_room_air_conditioner],
    temps={c.items.music_room_temperature: 1.0},
    humidities={c.items.music_room_humidity: 1.0}
)
