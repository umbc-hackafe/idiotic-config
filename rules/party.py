from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic import items, scheduler, modules, scenes

messages = {}

@bind(Command(items.party, "on"))
def party_start(evt):
    messages["party"] = modules.sign.new_message('PARTY     ', name='party', effects=['shake'], priority=.5)
    messages["time"] = modules.sign.new_message( '      TIME', name='time', effects=['shake'], priority=.5)

    items.black_light.on()

@bind(Command(items.party, "off"))
    if messages.get("party"):
        messages["party"].remove()
    if messages.get("time"):
        messages["time"].remove()

    items.black_light.off()
