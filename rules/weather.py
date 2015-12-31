from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

Scene("Daylight",
      active={i.name: (False, True) for i in items.with_tags(['nightlight'])},
      inactive={"outside_front_light": True,
                "outside_side_light": True})

MIN_DAY_BRIGHTNESS = 50
MAX_NIGHT_BRIGHTNESS = 40

@bind(Change(items.brightness))
def brightness_change(evt):
    if evt.old is None:
        return

    if evt.old < MIN_DAY_BRIGHTNESS < evt.new:
        scenes.daylight.enter()
    elif evt.old > MAX_NIGHT_BRIGHTNESS > evt.new:
        scenes.daylight.exit()

@bind(Schedule(scheduler.every().day.at("8:00")))
def enter_sun_mode(evt):
    if items.brightness.state >= MIN_DAY_BRIGHTNESS:
        scenes.daylight.enter()

@bind(Schedule(scheduler.every().day.at("19:00")))
def leave_sun_mode(evt):
    if items.brightness.state <= MAX_NIGHT_BRIGHTNESS:
        scenes.daylight.exit()
