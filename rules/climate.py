from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.item import Group
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

Group("Average Temperature",
      tags=("temperature",),
      state=lambda ms: sum((m.state for m in ms if m.state))/len([m for m in ms if m]),
      members=[i for i in items.all() if "temperature" in i.tags and "nyi" not in i.tags])

Group("Average Humidity",
      tags=("humidity",),
      state=lambda ms: sum((m.state for m in ms if m.state))/len([m for m in ms if m]),
      members=[i for i in items.all() if "humidity" in i.tags and "nyi" not in i.tags])

# Prevent furnace from turning on and of too quickly
@bind(Command(items.furnace, "on"))
def stop_furnace_flop(evt):
    pass

@bind(Change(items.average_temperature))
@bind(Change(items.minimum_temperature))
@bind(Change(items.maximum_temperature))
def temp_change(evt):
    current = items.average_temperature.state
    if current < items.minimum_temperature.state:
        items.furnace.on()
    elif current > items.maximum_temperature.state:
        items.furnace.off()

Scene("Daylight",
      active={i.name: (False, True) for i in items.with_tags(['nightlight'])},
      inactive={"outside_front_light": True,
                "outside_side_light": True})

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

@bind(Command(items.entertainment_room_laundry_room_door))
@augment(Delay(Command(items.entertainment_room_laundry_room_door, "on"),
         period=180,
         cancel=Command(items.entertainment_room_laundry_room_door, "off")))
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

@bind(Schedule(scheduler.every().day.at("8:00")))
def enter_sun_mode(evt):
    scenes.daylight.enter()

@bind(Schedule(scheduler.every().day.at("19:00")))
def leave_sun_mode(evt):
    scenes.daylight.exit()
