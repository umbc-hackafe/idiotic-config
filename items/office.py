from idiotic.item import Toggle, Trigger, Number, Group, Dimmer, display_unit
from idiotic import instance as c

Toggle("Office Light",
       bindings={"x10": {"code": "b4"}},
       tags=("office", "light"))

Trigger("Office Motion",
        tags=("office", "motion", "occupancy"))

Toggle("Office Door",
       display=Toggle.DisplayOpenClosed,
       tags=("office", "hallway", "door", "occupancy", "nyi"))

Number("Office Temperature",
       display=display_unit("C"),
       bindings={"http": {"pull": "pinkie:8081/temp"}},
       tags=("office", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))

Number("Office Humidity",
       display=Number.DisplayWholePercent,
       bindings={"http": {"pull": "pinkie:8081/hum"}},
       tags=("office", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))

Dimmer("Office Lamp 1",
       tags=("office", "light", "nyi"))

Dimmer("Office Lamp 2",
       tags=("office", "light", "nyi"))

Toggle("Office Air Conditioner",
       tags=("bedroom", "ac", "climate"),
       bindings={"modlet": {"device": "office",
                            "control": True}})

Group("Office Lights",
      tags=("office"),
      command_send=True,
      members=c.items.with_tags({'light', 'office'}))

c.modules.thermostat.Thermostat(
    "Office Thermostat",
    display=display_unit("C"),
    tags=("webui.show_disable", "heat", "nyi"),
    chillers=[c.items.office_air_conditioner],
    temps={c.items.office_temperature: 1.0},
    humidities={c.items.office_humidity: 1.0}
)
