from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic import items, scheduler, modules, scenes

@bind(Schedule(scheduler.every().day.at("7:30")))
def turtle_light_on(evt):
    items.turtle_light.on()

@bind(Schedule(scheduler.every().day.at("21:00")))
def turtle_light_off(evt):
    items.turtle_light.off()
