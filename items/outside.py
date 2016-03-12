from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Outside Side Light",
       tags=("outside", "light", "nightlight"),
       bindings={"x10": {"code": "a8"}})
Toggle("Outside Front Light",
       tags=("outside", "light", "nightlight"),
       bindings={"x10": {"code": "a9"}})
