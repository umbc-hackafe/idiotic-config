from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import instance as c

Scene("Server Work",
      active={"laundry_room_light": (True, True)})

Scene("Entertainment Room Sleep",
      active={"entertainment_room_light": (False, True)})

mapping = [
    (c.items.kitchen_motion, c.items.kitchen_light, 600),
    (c.items.kitchen_motion, c.items.kitchen_table_light, 600),
    (c.items.living_room_motion, c.items.living_room_lamp, 900),
    (c.items.hallway_motion, c.items.hallway_light, 120),
    (c.items.laundry_room_motion, c.items.laundry_room_light, 180),
    (c.items.entertainment_room_motion, c.items.entertainment_room_light, 300),
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

@bind(Command(c.items.entertainment_room_laundry_room_door))
@augment(Delay(Command(c.items.entertainment_room_laundry_room_door, "on"),
         period=180,
         cancel=Command(c.items.entertainment_room_laundry_room_door, "off")))
def laundry_door(evt):
    c.items.laundry_room_light.command("on" if evt.command == "off" else "off")

@bind(Command(c.items.bathroom_door))
@augment(Delay(Command(c.items.bathroom_door, "off"),
               period=10,
               cancel=Command(c.items.bathroom_door, "on")))
def bathroom_rule(evt):
    if evt.command == "on":
        c.items.bathroom_light.on()
    else:
        c.items.hallway_motion.on()
        c.items.hallway_motion.off()
        c.items.bathroom_light.off()

@bind(Command(c.items.garage_side_door))
@augment(Delay(Command(c.items.garage_side_door, "on"),
               period=1200))
def garage_light_rule(evt):
    if evt.command == "on":
        c.items.garage_lights.off()
    else:
        c.items.garage_lights.on()

#@bind(Change(c.items.garage_door))
def garage_light_thing(evt):
    if evt.new == evt.old:
        return
    if evt.new == True:
        c.items.garage_lights.off()
    else:
        if not scenes.daylight.active:
            c.items.garage_lights.on()
