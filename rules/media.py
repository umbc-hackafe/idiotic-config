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
    control = ((items.garage_lights, ("off", "on")),
               (items.garage_projector_screen, ("forward", "reverse")))

    def entered(self):
        items.garage_door_opener.off()
        for item, (act, _) in self.control:
            item.command(act)

    def exited(self):
        for item, (_, act) in self.control:
            item.command(act)
