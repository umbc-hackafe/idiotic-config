from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import modules, scheduler, items

Toggle("Living Room Lamp",
       tags=("living_room", "light", "nightlight"),
       bindings={"x10": {"code": "a6"}})
Toggle("Turtle Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a5"}})
Toggle("Living Room Air Conditioner",
       tags=("living_room", "ac", "climate"),
       bindings={"modlet": {"device": "living",
                            "control": True}})
Toggle("Front Door",
       tags=("living_room", "exterior_door", "occupancy", "nyi"))
Toggle("Living Room Motion",
        tags=("living_room", "motion", "occupancy"))
Toggle("Alert Beacon",
       tags=("living_room", "light", "notification"),
       bindings={"x10": {"code": "a11"}})
Toggle("Lava Lamp",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a12"}})
Toggle("Black Light",
       tags=("living_room", "light"),
       bindings={"x10": {"code": "a14"}})

Toggle("Living Room Projector",
       tags=("living_room", "media", "display"),
       bindings={"http": {"push": [
           ("on", "luna:8081/projector_on"),
           ("off", "luna:8081/projector_off")]}})

Number("Living Room Temperature",
       bindings={"http": {"pull": (60, "luna:8081/temp", None, float)}},
       tags=("living_room", "temperature", "climate", "webui.show_sparkline"))
Number("Living Room Humidity",
       bindings={"http": {"pull": (60, "luna:8081/hum", None, float)}},
       tags=("living_room", "humidity", "climate", "webui.show_sparkline"))

Scene("LivingRoomSleep",
      active={"living_room_projector": False,
              "living_room_lamp": (False, True),
              "kitchen_table_light": (False, True)})
