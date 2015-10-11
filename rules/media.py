from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic.item import Motor
from idiotic import items, scheduler, modules, scenes

sign_placeholder = None

living_room_media = Scene("LivingRoomMedia",
      active={"living_room_lamp": (False, True),
              "kitchen_table_light": (False, True)})

@living_room_media.on_enter
def do_sign_enter():
    global sign_placeholder
    items.living_room_projector.on(source='living_room_media')
    sign_placeholder = modules.sign.new_message('', priority=1, name='placeholder')

@living_room_media.on_exit
def do_sign_exit():
    global sign_placeholder
    if sign_placeholder:
        sign_placeholder.remove()
        sign_placeholder = None
    items.living_room_projector.off(source='living_room_media')

@bind(Change(items.living_room_projector))
def media_activate(evt):
    if evt.source == 'living_room_media':
        return

    if evt.new:
        scenes.livingroommedia.enter()
    else:
        scenes.livingroommedia.exit()

Scene("GarageMedia",
      active={"garage_lights": False,
              "garage_projector_screen": Motor.STOPPED_END,
              "garage_door_opener": False})
