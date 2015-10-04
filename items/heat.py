from idiotic.item import Toggle

Toggle("Furnace",
       tags=("heat",),
       bindings={"http": {"push": [
           ("on", "spike:8081/furnace?state=0"),
           ("off", "spike:8081/furnace?state=1")]}},
)
