from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import instance as c

Toggle("Living Room Lamp",
      tags=("living", "light"))

Toggle("Front Door",
       tags=("living", "door", "occupancy", "webui.readonly"))

Trigger("Living Room Motion",
        tags=("living", "motion", "webui.readonly"))

Number("Living Room Temperature",
       tags=("living", "temperature", "climate", "webui.readonly", "webui.show_sparkline"))

Number("Living Room Humidity",
       tags=("living", "humidity", "climate", "webui.readonly", "webui.show_sparkline"))
