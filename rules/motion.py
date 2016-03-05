from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

Scene("Server Work",
      active={"laundry_room_light": (True, True)})

Scene("Entertainment Room Sleep",
      active={"entertainment_room_light": (False, True)})

mapping = [
    (items.kitchen_motion, items.kitchen_light, 600),
    (items.kitchen_motion, items.kitchen_table_light, 600),
    (items.living_room_motion, items.living_room_lamp, 900),
    (items.hallway_motion, items.hallway_light, 120),
    (items.laundry_room_motion, items.laundry_room_light, 180),
    (items.entertainment_room_motion, items.entertainment_room_light, 300),
]

# This might not actually work with triggers rather than toggles for sensors
# at the very least, it's not very elegant otherwise...
for sensor, light, period in mapping:
    def closure(sensor, light, period):
        @bind(Command(sensor))
        @augment(Delay(Command(sensor, "off"), period=period,
                       cancel=Command(sensor, "on")))
        def rule(evt):
            light.command(evt.command)
    closure(sensor, light, period)

@bind(Command(items.entertainment_room_laundry_room_door))
@augment(Delay(Command(items.entertainment_room_laundry_room_door, "on"),
         period=180,
         cancel=Command(items.entertainment_room_laundry_room_door, "off")))
def laundry_door(evt):
    items.laundry_room_light.command("on" if evt.command == "off" else "off")

@bind(Command(items.bathroom_door))
@augment(Delay(Command(items.bathroom_door, "off"),
               period=10,
               cancel=Command(items.bathroom_door, "on")))
def bathroom_rule(evt):
    if evt.command == "on":
        items.bathroom_light.on()
    else:
        items.hallway_motion.on()
        items.hallway_motion.off()
        items.bathroom_light.off()

@bind(Command(items.garage_side_door))
@augment(Delay(Command(items.garage_side_door, "on"),
               period=1200))
def garage_light_rule(evt):
    if evt.command == "on":
        items.garage_lights.off()
    else:
        items.garage_lights.on()

#@bind(Change(items.garage_door))
def garage_light_thing(evt):
    if evt.new == evt.old:
        return
    if evt.new == True:
        items.garage_lights.off()
    else:
        if not scenes.daylight.active:
            items.garage_lights.on()
