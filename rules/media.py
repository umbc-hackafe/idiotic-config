from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

sign_placeholder = None

class LivingRoomMedia(Scene):
    control = (items.living_room_lamp, items.kitchen_table_light)
    def entered(self):
        global sign_placeholder
        items.living_room_projector.on(source='living_room_media')
        sign_placeholder = modules.sign.new_message('', priority=1, name='placeholder')
        for item in self.control:
            item.off()
            item.disable()

    def exited(self):
        global sign_placeholder
        for item in self.control:
            item.enable()
            item.on()
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

class GarageMedia(Scene):
    prev_garage_lights_state = False
    prev_garage_door_state = False

    def entered(self):
        prev_garage_lights_state = items.garage_lights.state
        prev_garage_door_state = items.garage_door.state
        items.garage_door_opener.off()
        items.garage_projector_screen.forward()
        items.garage_lights.off()

    def exited(self):
        items.garage_door.command("on" if prev_garage_door_state else "off")
        items.garage_lights.command("on" if prev_garage_lights_state else "off")
        items.garage_projector_screen.reverse()
