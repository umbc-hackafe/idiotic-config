from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Garage Lights",
       bindings={"x10": {"code": "c2"}},
       tags=("garage", "light"))

Trigger("Garage Door Opener",
        tags=("garage", "external_door"))

Toggle("Garage Door",
        tags=("garage", "external_door"))

Toggle("Garage Projector Screen",
       tags=("garage",))
