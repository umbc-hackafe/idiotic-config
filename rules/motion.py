from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

class Daylight(Scene):
    def entered(self):
        for item in items.with_tag('nightlight'):
            item.off()
            item.disable()

    def exited(self):
        for item in items.with_tag('nightlight'):
            item.enable()
            item.on()

mapping = [(items.kitchen_motion, items.kitchen_light),
           (items.living_room_motion, items.living_room_lamp),
           (items.hallway_motion, items.hallway_light),
           (items.laundry_room_motion, items.laundry_room_light)]

# This might not actually work with triggers rather than toggles for sensors
# at the very least, it's not very elegant otherwise...
for sensor, light in mapping:
    @bind(Command(sensor))
    @augment(Delay(Command(sensor, "OFF"), period=300,
             cancel=Command(sensor, "ON")))
    def rule(evt):
        light.command(evt.command)

@bind(Command(items.bathroom_door))
@augment(Delay(Command(items.bathroom_door, "OFF"),
               period=10,
               cancel=Command(items.bathroom_door, "ON")))
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
