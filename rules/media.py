from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.scene import Scene
from idiotic import items, scheduler, modules, scenes

class LivingRoomMedia(Scene):
    control = (items.living_room_lamp, items.kitchen_table_light)
    def entered(self):
        for item in self.control:
            item.off()
            item.disable()

    def exited(self):
        for item in self.control:
            item.enable()
            item.on()

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
