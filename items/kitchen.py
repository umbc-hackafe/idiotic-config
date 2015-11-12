from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Kitchen Light",
       tags=("kitchen", "light", "nightlight"),
       bindings={"x10": {"code": "a2"}})
Toggle("Kitchen Counter Light",
       tags=("kitchen", "light"),
       bindings={"x10": {"code": "a4"}})
Toggle("Kitchen Table Light",
       tags=("kitchen", "light", "nightlight"),
       bindings={"x10": {"code": "a3"}})
Toggle("Kitchen Stove Light",
       tags=("kitchen", "light"),
       bindings={"x10": {"code": "a7"}})
Toggle("Coffee Maker",
       tags=("kitchen", "food"),
       bindings={"modlet": {"device": "bedroom",
                            "control": True}})
Toggle("Kettle",
       tags=("kitchen", "food"),
       bindings={"http": {"push": [
           ("on", "kimiko.hackafe.net/teakettle/hold/600"),
           ("off", "kimiko.hackafe.net/teakettle/hold/1")
           ]}})

Number("Kettle Temperature",
       tags=("kitchen", "food"),
       bindings={"http": {"push": [
           ("set", "kimiko.hackafe.net/teakettle/heat/{state}")
           ]}})

Number("Kettle Current",
       tags=("kitchen", "food"))

Toggle("Kitchen Door",
       tags=("kitchen", "exterior_door", "occupancy", "nyi"))

Toggle("Kitchen Motion",
       tags=("kitchen", "motion", "occupancy"),
       ignore_redundant=True)
