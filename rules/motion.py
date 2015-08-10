from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

class Daylight(Scene):
    def entered(self):
        for item in items.with_tags(['nightlight']):
            item.off()
            item.disable()

    def exited(self):
        for item in items.with_tags(['nightlight']):
            item.enable()
            item.on()

mapping = [(items.kitchen_motion, items.kitchen_light, 600),
           (items.kitchen_motion, items.kitchen_table_light, 600),
           (items.living_room_motion, items.living_room_lamp, 300),
           (items.hallway_motion, items.hallway_light, 120),
           (items.laundry_room_motion, items.laundry_room_light, 180)]

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

@bind(Command(items.entertainment_room__laundry_room_door))
@augment(Delay(Command(items.entertainment_room__laundry_room_door, "on"),
         period=180,
         cancel=Command(items.entertainment_room__laundry_room_door, "off")))
def laundry_door(evt):
    items.laundry_room_light.command("on" if evt.command == "off" else "off")
    items.entertainment_room_light.command("on" if evt.command == "off" else "off")

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

@bind(Schedule(scheduler.every().day.at("8:00")))
def enter_sun_mode(evt):
    scenes.daylight.enter()

@bind(Schedule(scheduler.every().day.at("19:00")))
def leave_sun_mode(evt):
    scenes.daylight.exit()
