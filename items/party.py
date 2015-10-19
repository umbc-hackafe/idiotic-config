from idiotic.item import Toggle, Trigger, Number, Group
from idiotic.scene import Scene
from idiotic import modules, scheduler, items

Toggle("Fog Machine",
       tags=("garage",),
       bindings={"http": {"push": [
           ("on", "discord:8081/fog?state=0"),
           ("off", "discord:8081/fog?state=1")]}})
