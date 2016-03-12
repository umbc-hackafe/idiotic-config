from idiotic.item import Toggle, Trigger, Number, Group

Number("Brightness",
       bindings={"http": {"pull": (30, "luna:8081/lx", None, float)}},
       tags=("weather", "climate", "webui.show_sparkline"))
