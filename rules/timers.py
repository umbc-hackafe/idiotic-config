from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic import instance as c
import random

@bind(Schedule(c.scheduler.every().day.at("7:30")))
def turtle_light_on(evt):
    c.items.turtle_light.on()

@bind(Schedule(c.scheduler.every().day.at("21:00")))
def turtle_light_off(evt):
    c.items.turtle_light.off()

@bind(Command(c.items.do_something))
def do_a_thing(evt):
    item = random.choice(list(c.items.all()))
    command = random.choice(list(item.commands()))
    try:
        getattr(item, command)()
        modules.sign.new_message("Did {} {}!".format(item.name, command), effects=["scroll"], lifetime=10, name="idiotic.dosomething")
    except:
        try:
            arg = random.randint(0, 30)
            getattr(item, command)(arg)
            modules.sign.new_message("Did {} {}({})!".format(item.name, command, arg), effects=["scroll"], lifetime=10, name="idiotic.dosomething")
        except:
            modules.sign.new_message("Couldn't do anything :(", effects=["scroll"], lifetime=10, name="idiotic.dosomething")
