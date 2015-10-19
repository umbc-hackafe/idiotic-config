from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

messages = {}

party = Scene("Party",
      active={"living_room_lamp": (False, True),
              "kitchen_table_light": (False, True),
              "kitchen_light": (False, True),
              "black_light": True,
              "disco_lights": True,
              "alert_beacon": True,
              "lava_lamp": True,
              "fog_machine": True})

@party.on_enter
def party_start():
    messages["party"] = modules.sign.new_message('PARTY     ', name='party', effects=['shake'], priority=.5)
    messages["time"] = modules.sign.new_message( '      TIME', name='time', effects=['shake'], priority=.5)

@party.on_exit
def party_end():
    if messages.get("party"):
        messages["party"].remove()
    if messages.get("time"):
        messages["time"].remove()
