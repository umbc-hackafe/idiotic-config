from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Office Light",
       bindings={"x10": {"code": "b4"}},
       tags=("office", "light"))

Trigger("Office Motion",
        tags=("office", "motion", "occupancy"))

Toggle("Office Door",
       tags=("office", "hallway", "door", "occupancy", "nyi"))

Number("Office Temperature",
       bindings={"http": {"pull": "pinkie:8081/temp"}},
       tags=("office", "temperature", "climate", "webui.show_sparkline",
           "webui.readonly"))

Number("Office Humidity",
       bindings={"http": {"pull": "pinkie:8081/hum"}},
       tags=("office", "humidity", "climate", "webui.show_sparkline",
           "webui.readonly"))

Toggle("Office Air Conditioner",
       tags=("office", "ac", "climate", "nyi"))
