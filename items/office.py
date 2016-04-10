from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Office Light",
       tags=("office", "light"))

Trigger("Office Motion",
        tags=("office", "motion", "occupancy", "webui.readonly"))

Toggle("Office Door",
       tags=("office", "door", "occupancy", "webui.readonly"))

Number("Office Temperature",
       tags=("office", "temperature", "climate", "webui.readonly", "webui.show_sparkline"))

Number("Office Humidity",
       tags=("office", "humidity", "climate", "webui.readonly", "webui.show_sparkline"))
