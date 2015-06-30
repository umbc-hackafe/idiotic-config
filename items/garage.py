from idiotic.item import Toggle, Trigger, Number, Group, Motor
from idiotic import modules, scheduler

Toggle("Garage Lights",
       bindings={"x10": {"code": "c2"}},
       tags=("garage", "light"))

Toggle("Garage Door Opener",
       bindings={"http":
                 {"on": "thegreatandpowerfultrixie:8081/door?action=trigger",
                  "off": "thegreatandpowerfultrixie:8081/door?action=close"}},
       tags=("garage", "external_door"))

Toggle("Garage Door",
        tags=("garage", "external_door"))

Motor("Garage Projector Screen",
      constrained=True,
      bindings={"http":
                {"forward": "thegreatandpowerfultrixie:8081/projector?action=down",
                 "reverse": "thegreatandpowerfultrixie:8081/projector?action=up",
                 "stop": "thegreatandpowerfultrixie:8081/projector?action=stop"}},
      tags=("garage",))
