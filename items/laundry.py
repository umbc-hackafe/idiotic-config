from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Laundry Room Light",
       tags=("laundry_room", "light"),
       bindings={"x10": {"code": "a10"}})

Trigger("Laundry Room Motion",
        tags=("laundry_room", "motion", "occupancy"))

Toggle("Laundry Room Door",
       display=Toggle.DisplayOpenClosed,
       tags=("laundry_room", "exterior_door", "occupancy", "nyi"))
