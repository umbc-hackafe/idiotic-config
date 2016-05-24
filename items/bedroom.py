from idiotic.item import Toggle, Trigger, Number, Group, Dimmer, display_unit
from idiotic import instance as c

Dimmer("Bedroom Desk Lamp",
       bindings={"wink": {"name": "Dylan Desk"}},
       tags=("bedroom", "light", "alexa.exclude_iot"))

Toggle("Bedroom Light",
       bindings={"http": {"push": "rarity:8081/downlight"}},
       tags=("bedroom", "light"),
       ignore_redundant=True)

Toggle("Bedroom Mood Light",
       tags=("bedroom", "light", "nyi"))

Toggle("Bedroom Fan",
       bindings={"http": {"push": [("on", "rarity:8081/high"),
                                   ("off", "rarity:8081/fanoff")]}},
       tags=("bedroom", "fan", "climate"))

Toggle("Bedroom Air Conditioner",
       tags=("bedroom", "ac", "climate"),
       bindings={"modlet": {"device": "bedroom",
                            "control": True}})
Trigger("Bedroom Motion",
        tags=("bedroom", "motion", "occupancy", "nyi"))

Toggle("Bedroom Door",
        tags=("bedroom", "hallway", "door", "occupancy", "nyi"))

Number("Bedroom Temperature",
       display=display_unit("C"),
       bindings={"http": {"pull": (60, "rarity:8081/temp", None, float)}},
       tags=("bedroom", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))

Number("Bedroom Humidity",
       display=Number.DisplayWholePercent,
       bindings={"http": {"pull": (60, "rarity:8081/hum", None, float)}},
       tags=("bedroom", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))

c.modules.thermostat.Thermostat(
    "Bedroom Thermostat",
    display=display_unit("C"),
    tags=("webui.show_disable", "heat"),
    chillers=[c.items.bedroom_air_conditioner],
    temps={c.items.bedroom_temperature: 1.0},
    humidities={c.items.bedroom_humidity: 1.0}
)
