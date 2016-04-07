from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import instance as c

Group("Living Room Lamp",
      tags=("living_room", "light", "nightlight"),
      commands=False,
      command_send=True)

Toggle("Turtle Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a5"}})

livingRoomAC = Toggle("Living Room Air Conditioner",
       bindings={"modlet": {"device": "garage",
                            "control": True}},
       tags=("living_room", "ac", "climate"))

Toggle("Front Door",
       tags=("living_room", "exterior_door", "occupancy", "nyi"))
Trigger("Living Room Motion",
        tags=("living_room", "motion", "occupancy"))
Toggle("Alert Beacon",
       tags=("living_room", "light", "notification", "nyi"))
Toggle("Lava Lamp",
       tags=("living_room", "light", "nyi"))
Toggle("Black Light",
       tags=("living_room", "light", "nyi"))
Toggle("Disco Lights",
       tags=("living_room", "light", "nyi"))
Toggle("Other Disco Lights",
       tags=("living_room", "light", "nyi"))

for item in [c.items.lamp_blue,
             c.items.lamp_white,
             c.items.lamp_green,
             c.items.lamp_grellow,
             c.items.lamp_dark_blue]:
    c.items.living_room_lamp.add(item)
    item.tags.update(('living_room', 'light'))

c.items.corner_light.tags.update(('living_room', 'light'))
c.items.record_light.tags.update(('living_room', 'light'))

Group("Living Room Lights",
      tags=("living_room", "light"),
      command_send=True,
      members=c.items.with_tags({'light', 'living_room'}))

Toggle("Luna",
       tags=("interaction",),
       bindings={"avaya": {"port": "15"}})

Toggle("Living Room Camera",
       tags=("interaction",),
       bindings={"avaya": {"port": "48"}})

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

c.modules.thermostat.Thermostat("Living Room AC",
       tags=("webui.show_disable",
             "heat",),
       chillers=[
           livingRoomAC,
       ],
       temps={
                c.items.living_room_temperature: 1.0,
           },
       humidities={
                c.items.living_room_humidity: 1.0,
           },
     )

