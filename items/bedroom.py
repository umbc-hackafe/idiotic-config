from idiotic.item import Toggle, Trigger, Number, Group, Dimmer
from idiotic import instance as c

Dimmer("Bedroom Desk Lamp",
       bindings={"wink": {"name": "Dylan Desk"}},
       tags=("bedroom", "light", "alexa.exclude_iot"))

Toggle("Bedroom Light",
       bindings={"http": {"push": "rarity:8081/downlight"}},
       tags=("bedroom", "light"),
       disable_commands=("on", "off"),
       ignore_redundant=True)

Toggle("Bedroom Mood Light",
       tags=("bedroom", "light", "nyi"))

Toggle("Bedroom Fan",
       tags=("bedroom", "fan", "climate", "nyi"))

Toggle("Bedroom Air Conditioner",
       tags=("bedroom", "ac", "climate"),
       bindings={"modlet": {"device": "bedroom",
                            "control": True}})
Trigger("Bedroom Motion",
        tags=("bedroom", "motion", "occupancy", "nyi"))

Toggle("Bedroom Door",
        tags=("bedroom", "hallway", "door", "occupancy", "nyi"))

Number("Bedroom Temperature",
       bindings={"http": {"pull": (60, "rarity:8081/temp", None, float)}},
       tags=("bedroom", "temperature", "climate", "webui.show_sparkline"))

Number("Bedroom Humidity",
       bindings={"http": {"pull": (60, "rarity:8081/hum", None, float)}},
       tags=("bedroom", "humidity", "climate", "webui.show_sparkline"))
