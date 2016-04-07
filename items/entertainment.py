from idiotic.item import Toggle, Trigger, Number, Group

Toggle("Entertainment Room Light",
       bindings={"x10": {"code": "a13"}},
       tags=("entertainment_room", "light"))
Toggle("Entertainment Room Air Conditioner",
       tags=("entertainment_room", "ac", "climate"))
Toggle("Entertainment Room Living Room Door",
       tags=("entertainment_room", "living_room", "door", "occupancy", "nyi"))

Toggle("Entertainment Room Laundry Room Door",
       tags=("entertainment_room", "laundry_room", "door", "occupancy"))
Trigger("Entertainment Room Motion",
        tags=("entertainment_room", "motion", "occupancy"))

Number("Entertainment Room Temperature",
       bindings={"http": {"pull": (60, "vinyl:8081/temp", None, float)}},
       tags=("entertainment_room", "temperature", "climate", "webui.show_sparkline"))
Number("Entertainment Room Humidity",
       bindings={"http": {"pull": (60, "vinyl:8081/hum", None, float)}},
       tags=("entertainment_room", "humidity", "climate", "webui.show_sparkline"))
