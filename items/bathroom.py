from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Toggle("Bathroom Light",
       tags=("bathroom", "light"),
       bindings={"x10": {"code": "b3"}})

Toggle("Bathroom Door",
       tags=("bathroom", "door"),
       bindings={"sign": ("on", {"message": "Bathroom Occupied", "effects": ["bounce_x"]}, "off")})
