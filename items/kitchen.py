from idiotic.item import Toggle, Trigger, Number, Group, Text

Toggle("Kitchen Light",
       tags=("kitchen", "light"))

Toggle("Kitchen Door",
       tags=("kitchen", "door", "webui.readonly"))

Trigger("Kitchen Motion",
       tags=("kitchen", "motion", "occupancy", "webui.readonly"))

Number("Kitchen Temperature",
       tags=("kitchen", "temperature", "climate", "webui.readonly", "webui.show_sparkline"))

Number("Kitchen Humidity",
       tags=("kitchen", "humidity", "climate", "webui.readonly", "webui.show_sparkline"))
