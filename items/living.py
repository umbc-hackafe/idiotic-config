from idiotic.item import Toggle, Trigger, Number, Group, Dimmer, display_unit
from idiotic.scene import Scene
from idiotic import instance as c

Group("Living Room Lamp",
      display=Toggle.DisplayOnOff,
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
       display=Toggle.DisplayOpenClosed,
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

for name in ["Lamp Blue", "Lamp White", "Lamp Green", "Lamp Grellow", "Lamp Dark Blue"]:
    Dimmer(name,
           bindings={"wink": {}},
           groups=[c.items.living_room_lamp],
           tags=('living_room', 'light', 'alexa.iot_exclude'))

Group("Living Room Lights",
    display=Toggle.DisplayOnOff,
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
       display=display_unit("C"),
       bindings={"http": {"pull": (60, "luna:8081/temp", None, float)}},
       tags=("living_room", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))
Number("Living Room Humidity",
       display=Number.DisplayWholePercent,
       bindings={"http": {"pull": (60, "luna:8081/hum", None, float)}},
       tags=("living_room", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))

c.modules.thermostat.Thermostat("Living Room Thermostat",
       display=display_unit("C"),
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

