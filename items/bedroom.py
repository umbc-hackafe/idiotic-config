from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import instance as c

Toggle("Bedroom Light",
       tags=("bedroom", "light"))

Toggle("Bedroom Fan",
       tags=("bedroom", "fan"))

Toggle("Bedroom AC",
       tags=("bedroom", "climate"))

Trigger("Bedroom Motion",
        tags=("webui.readonly",))

Toggle("Bedroom Door",
        tags=("bedroom", "webui.readonly"))

Number("Bedroom Temperature",
       tags=("bedroom", "temperature", "webui.readonly", "webui.show_sparkline"))

Number("Bedroom Humidity",
       tags=("bedroom", "humidity", "webui.readonly" "webui.show_sparkline"))
