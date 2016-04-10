from idiotic.item import Toggle
from idiotic import instance as c
from idiotic.modutils import require_items

require_items("living")
require_items("bedroom")
require_items("office")
require_items("kitchen")

Toggle("Furnace",
       tags=("heat", "webui.show_disable")
      )

c.modules.thermostat.Thermostat("Thermostat",
       tags=("webui.show_disable",
             "heat",),
       heaters=[
           c.items.furnace,
       ],
       temps={
                c.items.living_room_temperature: 1,
                c.items.office_temperature: 1,
                c.items.bedroom_temperature: 1,
                c.items.kitchen_temperature: 1,
           },
       humidities={
                c.items.living_room_humidity: 0.16,
                c.items.office_humidity: 0.16,
                c.items.bedroom_humidity: 0.16,
                c.items.kitchen_humidity: 0.16,
           },
     )

