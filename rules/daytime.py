from idiotic.rule import bind, Schedule
from idiotic import instance as c

@bind(Schedule(c.scheduler.every().day.at("8:00")))
def enter_sun_mode(evt):
    scenes.daylight.enter()

@bind(Schedule(c.scheduler.every().day.at("19:00")))
def leave_sun_mode(evt):
    scenes.daylight.exit()
