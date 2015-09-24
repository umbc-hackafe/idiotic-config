from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic import items, scheduler, modules, scenes

@bind(Schedule(scheduler.every().day.at("7:30")))
def turtle_light_on(evt):
    items.turtle_light.on()

@bind(Schedule(scheduler.every().day.at("21:00")))
def turtle_light_off(evt):
    items.turtle_light.off()

reminders = {}

@bind(Schedule(scheduler.every().thursday.at("18:00")))
def recycling_reminder(evt):
    reminders["recycling"] = modules.sign.new_message("RECYCLING", effects=["bounce_x", "shake"])

@bind(Schedule(scheduler.every().monday.at("18:00")))
def trash_reminder(evt):
    reminders["trash"] = modules.sign.new_message("TRASH", effects=["bounce_x", "shake"])

@bind(Schedule(scheduler.every().friday.at("8:00")))
@bind(Command(items.garbage))
def recycling_done(evt):
    if reminders.get("recycling"):
        reminders["recycling"].remove()

@bind(Schedule(scheduler.every().tuesday.at("8:00")))
@bind(Command(items.garbage))
def trash_done(evt):
    if reminders.get("trash"):
        reminders["trash"].remove()
