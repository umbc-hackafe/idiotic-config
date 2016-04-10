from idiotic.rule import bind, Schedule
from idiotic.scene import Scene
from idiotic import instance as c

Scene("Daytime")

@bind(Schedule(c.scheduler.every().day.at("8:00")))
def enter_sun_mode(evt):
    scenes.daylight.enter()

@bind(Schedule(c.scheduler.every().day.at("19:00")))
def leave_sun_mode(evt):
    scenes.daylight.exit()
