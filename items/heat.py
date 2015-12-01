from idiotic.item import Toggle, Number

Toggle("Furnace",
       tags=("heat",),
       bindings={"x10": {"code": "d1"}}
#       bindings={"http": {"push": [
#           ("on", "spike:8081/furnace?state=0"),
#           ("off", "spike:8081/furnace?state=1")]}},
)

Number("Minimum Temperature",
       tags=("heat",))

Number("Maximum Temperature",
       tags=("heat",))
