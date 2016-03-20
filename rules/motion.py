from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.declare import Rule, StateIsCondition, StateBetweenCondition, ItemLambdaCondition, CommandReceivedCondition, CommandAction
from idiotic.scene import Scene
from idiotic.timer import Timer
from idiotic import instance as c
import functools

Scene("Entertainment Room Sleep")
Scene("Living Room Sleep")
Scene("Music Room Sleep")
Scene("Bedroom Sleep")
Scene("Office Sleep")

Scene("Living Room Media")

Scene("Kitchen Occupied")
Scene("Living Room Occupied")
Scene("Entertainment Room Occupied")
Scene("Laundry Room Occupied")
Scene("Bathroom Occupied")
Scene("Music Room Occupied")
Scene("Bedroom Occupied")
Scene("Office Occupied")

mapping = [
    (c.items.kitchen_motion, c.items.kitchen_light, 600),
    (c.items.kitchen_motion, c.items.kitchen_table_light, 600),
    (c.items.living_room_motion, c.items.living_room_lamp, 900),
    (c.items.hallway_motion, c.items.hallway_light, 120),
    (c.items.laundry_room_motion, c.items.laundry_room_light, 180),
    (c.items.entertainment_room_motion, c.items.entertainment_room_light, 300),
]

# When any of:
#   - Kitchen door was opened within one minute
#   - Kitchen motion sensor was activated within 1 minute
# Do:
#   Enter scene KitchenOccupied
Rule(CommandReceivedCondition(c.items.kitchen_motion, 600, 'on') |
     CommandReceivedCondition(c.items.kitchen_door, 60, 'on'),
     SceneAction(
     both=[CommandAction(c.items.kitchen_light, yes='on', no='off'),
           CommandAction(c.items.kitchen_table_light, yes='on', no='off')])


# This might not actually work with triggers rather than toggles for sensors
# at the very least, it's not very elegant otherwise...
for sensors, light, period in mapping:
    if isinstance(sensor, list):
        pass
    else:
        conditions = CommandReceivedCondition(sensor, period, 'on')
    Rule(CommandReceivedCondition(sensor, period, 'on'),
      CommandAction(light, yes='on', no='off'))

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

#Rule(
#    StateBetweenCondition(c.items.average_temperature, 10, 20),
#    yes=functools.partial(print, "IT IS TRUE"),
#    no=functools.partial(print, "IT IS NOT TRUE")
#)

Rule(CommandReceivedCondition(c.items.lava_lamp, 5, 'on'),
      CommandAction(c.items.entertainment_room_light, yes='on', no='off'))
