from idiotic.item import Toggle, Trigger, Number, Group, Motor

Toggle("Garage Lights",
       bindings={"x10": {"code": "c8"}},
       tags=("garage", "light"))

Toggle("Garage Counter Lights",
       tags=("garage", "light", "nyi"))

Toggle("Garage Purple Lights",
       tags=("garage", "light", "nyi"))

Toggle("Garage Door",
       display=Toggle.DisplayOpenClosed,
       bindings={"http": {
           "pull": (15, "thegreatandpowerfultrixie:8081/door?action=get", None, lambda s: s.startswith("OPEN")),
           "push": [
               ("on", "thegreatandpowerfultrixie:8081/door?action=trigger"),
               ("off", "thegreatandpowerfultrixie:8081/door?action=close")]}},
       tags=("garage", "external_door"),
       aliases={"open": "on", "close": "off"})

Motor("Garage Projector Screen",
      display=Motor.DisplayDownUp,
      constrained=True,
      bindings={"http": {"push": [
          ("forward", "thegreatandpowerfultrixie:8081/screen?action=down"),
          ("reverse", "thegreatandpowerfultrixie:8081/screen?action=up"),
          ("stop", "thegreatandpowerfultrixie:8081/screen?action=stop")]}},
      aliases={"down": "forward", "up": "reverse"},
      tags=("garage",))

Toggle("Garage Air Conditioner",
       tags=("garage", "ac", "climate", "nyi"))

Toggle("Garage Side Door",
       display=Toggle.DisplayClosedOpen,
       tags=("garage", "external_door"))
