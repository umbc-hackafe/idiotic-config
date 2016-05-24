from idiotic.item import Toggle, Trigger, Number, Group, Dimmer, display_unit
from idiotic import instance as c

Dimmer("Hall Light 1",
       bindings={"wink": {}},
       tags=("hallway", "light"))

Dimmer("Hall Light 2",
       bindings={"wink": {}},
       tags=("hallway", "light"))

Group("Hallway Light",
      display=Toggle.DisplayOnOff,
      tags=("hallway", "light", "nightlight"),
      commands=False,
      command_send=True,
      members=[c.items.hall_light_1, c.items.hall_light_2])

Trigger("Hallway Motion",
        tags=("hallway", "motion", "occupancy"))

Number("Hallway Temperature",
       display=display_unit("C"),
       bindings={"http": {"pull": (60, "scootaloo:8081/temp", None, float)}},
       tags=("hallway", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))
Number("Hallway Humidity",
       display=Number.DisplayWholePercent,
       bindings={"http": {"pull": (60, "scootaloo:8081/hum", None, float)}},
       tags=("hallway", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))
