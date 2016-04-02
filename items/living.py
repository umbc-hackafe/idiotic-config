from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import instance as c

Toggle("Living Room Lamp",
       tags=("living_room", "light", "nightlight"),
       bindings={"x10": {"code": "a6"}})
Toggle("Turtle Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a5"}})
Toggle("Living Room Air Conditioner",
       bindings={"modlet": {"device": "garage",
                            "control": True}},
       tags=("living_room", "ac", "climate"))

Toggle("Front Door",
       tags=("living_room", "exterior_door", "occupancy", "nyi"))
Toggle("Living Room Motion",
        tags=("living_room", "motion", "occupancy"))
Toggle("Alert Beacon",
       tags=("living_room", "light", "notification"),
       bindings={"x10": {"code": "a11"}})
Toggle("Lava Lamp",
       tags=("living_room", "light"))
Toggle("Black Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a14"}})
Toggle("Disco Lights",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a15"},
                 "modlet": {"device": "living",
                            "control": True}})
Toggle("Other Disco Lights",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a1"}})
Toggle("Corner Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a12"}})

c.items.lamp_blue.tags.update(('living_room', 'light'))
c.items.lamp_dark_blue.tags.update(('living_room', 'light'))
c.items.record_light.tags.update(('living_room', 'light'))

Group("Living Room Lights",
      tags=("living_room", "light"),
      command_send=True,
      members=c.items.with_tags({'light', 'living_room'}))

Toggle("Luna",
       tags=("interaction",),
       bindings={"avaya": {"port": "15"}})

Toggle("Living Room Projector",
       tags=("living_room", "media", "display"),
       bindings={"http": {"push": [
           ("on", "luna:8081/projector_on"),
           ("off", "luna:8081/projector_off")]}})

Number("Living Room Temperature",
       bindings={"http": {"pull": (60, "luna:8081/temp", None, float)}},
       tags=("living_room", "temperature", "climate", "webui.show_sparkline"))
Number("Living Room Humidity",
       bindings={"http": {"pull": (60, "luna:8081/hum", None, float)}},
       tags=("living_room", "humidity", "climate", "webui.show_sparkline"))

