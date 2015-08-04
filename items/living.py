from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Living Room Lamp",
       tags=("living_room", "light", "nightlight"),
       bindings={"x10": {"code": "a6"}})
Toggle("Turtle Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a5"}})
Toggle("Living Room AC",
       tags=("living_room", "ac", "climate"),
       bindings={"modlet": {"device": "living"}})
Toggle("Front Door",
       tags=("living_room", "exterior_door", "occupancy", "nyi"))
Toggle("Living Room Motion",
        tags=("living_room", "motion", "occupancy"))
Toggle("Alert Beacon",
       tags=("living_room", "light", "notification"),
       bindings={"x10": {"code": "a11"}})
Toggle("Lava Lamp",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a12"}})

Toggle("Living Room Projector",
       tags=("living_room", "media", "display"),
       bindings={"http": {"push": [
           ("on", "luna:8081/projector_on"),
           ("off", "luna:8081/projector_off")]}})

Number("Living Room Temperature",
       bindings={"http": {"pull": "luna:8081/temp"}},
       tags=("living_room", "temperature", "climate", "webui.show_sparkline"))
Number("Living Room Humidity",
       bindings={"http": {"pull": "luna:8081/hum"}},
       tags=("living_room", "humidity", "climate", "webui.show_sparkline"))
