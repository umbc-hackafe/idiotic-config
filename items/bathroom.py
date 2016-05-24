from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Bathroom Light",
       tags=("bathroom", "light"),
       bindings={"x10": {"code": "b3"}})

Toggle("Bathroom Door",
       display=Toggle.DisplayOpenClosed,
       tags=("bathroom", "door"),
       bindings={"sign": {"commands": ("on", {"message": "Bathroom Occupied", "effects": ["bounce_x"]}, "off")}})
