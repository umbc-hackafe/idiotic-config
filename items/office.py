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

Toggle("Office Air Conditioner",
       tags=("office", "ac", "climate", "nyi"))
