from idiotic.item import Toggle, Trigger, Number, Group, Text

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
       tags=("kitchen", "light", "nyi"),
       bindings={"x10": {"code": "a7"}})
Toggle("Coffee Maker",
       tags=("kitchen", "food", "nyi"))
Toggle("Kettle",
       tags=("kitchen", "food", "nyi"),
       bindings={"http": {"push": [
           ("on", "kimiko.hackafe.net/teakettle/hold/600"),
           ("off", "kimiko.hackafe.net/teakettle/hold/1")
           ]}})

Number("Kettle Temperature",
       tags=("kitchen", "food", "nyi"),
       bindings={"http": {"push": [
           ("set", "kimiko.hackafe.net/teakettle/heat/{state}")
           ]}})

Number("Kettle Current",
       tags=("kitchen", "food", "nyi"))

Text("Kettle Status",
     tags=("kitchen", "food", "nyi"),
     ignore_redundant=True,
     bindings={"sign": {"state": {"message": "{state}", "effects": ["scroll"], "lifetime": 10}}})

Toggle("Kitchen Door",
       tags=("kitchen", "exterior_door", "occupancy", "nyi"))

Trigger("Kitchen Motion",
       tags=("kitchen", "motion", "occupancy"),
       ignore_redundant=True)
