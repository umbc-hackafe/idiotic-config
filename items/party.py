from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import modules, scheduler, items

Toggle("Fog Machine",
       tags=("garage",),
       bindings={"http": {"push": [
           ("on", "discord:8081/fog?state=0"),
           ("off", "discord:8081/fog?state=1")]}})

Number("Living Room Temperature",
       bindings={"http": {"pull": (60, "luna:8081/temp", None, float)}},
       tags=("living_room", "temperature", "climate", "webui.show_sparkline"))
Number("Living Room Humidity",
       bindings={"http": {"pull": (60, "luna:8081/hum", None, float)}},
       tags=("living_room", "humidity", "climate", "webui.show_sparkline",
             "webui.enable_graph"))

Scene("LivingRoomSleep",
      active={"living_room_projector": False,
              "living_room_lamp": (False, True),
              "kitchen_table_light": (False, True)})
