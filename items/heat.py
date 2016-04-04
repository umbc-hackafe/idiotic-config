from idiotic.item import Toggle, Number
from idiotic import instance as c
from idiotic.modutils import require_items

require_items('living')
require_items('office')
require_items('bedroom')
require_items('music')
require_items('entertainment')
require_items('hall')

Toggle("Furnace",
       tags=("heat", "webui.show_disable"),
       bindings={"x10": {"code": "d1"}}
      )

c.modules.thermostat.Thermostat("Boiler",
       tags=("webui.show_disable",
             "heat",),
       heaters=[
           c.items.furnace,
       ],
       temps={
                c.items.living_room_temperature: 1,
                c.items.office_temperature: 1,
                c.items.bedroom_temperature: 1,
#                c.items.music_room_temperature: 1,
                c.items.entertainment_room_temperature: 1,
                c.items.hallway_temperature: 1,
           },
       humidities={
                c.items.living_room_humidity: 0.16,
                c.items.office_humidity: 0.16,
                c.items.bedroom_humidity: 0.16,
                c.items.music_room_humidity: 0.16,
                c.items.entertainment_room_humidity: 0.16,
                c.items.hallway_humidity: 0.16,
           },
     )

