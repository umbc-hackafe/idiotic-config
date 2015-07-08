from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic import items, scheduler, modules, scenes

MIN_DAY_BRIGHTNESS = 15
MAX_NIGHT_BRIGHTNESS = 5

@bind(Change(items.brightness))
def brightness_change(evt):
    if evt.old is None:
        return

    if evt.old < MIN_DAY_BRIGHTNESS < evt.new:
        scenes.daylight.enter()
    elif evt.old > MAX_NIGHT_BRIGHTNESS > evt.new:
        scenes.daylight.exit()
