from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes
import requests

messages = {}

party = Scene("Party",
      active={"living_room_lamp": (False, True),
              "kitchen_table_light": (False, True),
              "kitchen_light": (False, True),
              "black_light": True,
              "disco_lights": True,
              "alert_beacon": True,
              "lava_lamp": True,
              "fog_machine": True,
              "kitchen_counter_lights": True})

@party.on_enter
def party_start():
    messages["party"] = modules.sign.new_message('PARTY     ', name='party', effects=['shake'], priority=.5)
    messages["time"] = modules.sign.new_message( '      TIME', name='time', effects=['shake'], priority=.5)
    requests.get("http://celestia.hackafe.net/clear")
    requests.post("http://celestia.hackafe.net/add_saved_animation/Rainbow")
    requests.get("http://thegreatandpowerfultrixie.hackafe.net/clear")
    requests.post("http://thegreatandpowerfultrixie.hackafe.net/add_saved_animation/Rainbow")

@party.on_exit
def party_end():
    if messages.get("party"):
        messages["party"].remove()
    if messages.get("time"):
        messages["time"].remove()
    requests.get("http://thegreatandpowerfultrixie.hackafe.net/clear")
    requests.get("http://celestia.hackafe.net/clear")
