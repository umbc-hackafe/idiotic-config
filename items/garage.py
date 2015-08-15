from idiotic.item import Toggle, Trigger, Number, Group, Motor
from idiotic import modules, scheduler

Toggle("Garage Lights",
       bindings={"x10": {"code": "c2"}},
       tags=("garage", "light"))

Toggle("Garage Counter Lights",
       bindings={"x10": {"code": "c3"}},
       tags=("garage", "light"))

Toggle("Garage Door Opener",
       bindings={"http": {"push": [
           ("on", "thegreatandpowerfultrixie:8081/door?action=trigger"),
           ("off", "thegreatandpowerfultrixie:8081/door?action=close")]}},
       tags=("garage", "external_door"))

Toggle("Garage Door",
       bindings={"http": {"pull": (15, "thegreatandpowerfultrixie:8081/door?action=get", None, lambda s: s.startswith("OPEN"))}},
       tags=("garage", "external_door"))

Motor("Garage Projector Screen",
      constrained=True,
      bindings={"http": {"push": [
          ("forward", "thegreatandpowerfultrixie:8081/screen?action=down"),
          ("reverse", "thegreatandpowerfultrixie:8081/screen?action=up"),
          ("stop", "thegreatandpowerfultrixie:8081/screen?action=stop")]}},
      tags=("garage",))

Toggle("Garage AC",
       tags=("garage", "ac", "climate"),
       bindings={"modlet": {"device": "garage",
                            "control": True}})
