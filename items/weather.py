from idiotic.item import Toggle, Trigger, Number, Group, display_unit

Number("Brightness",
       display=display_unit("lx"),
       bindings={"http": {"pull": (30, "luna:8081/lx", None, float)}},
       tags=("weather", "climate", "webui.show_sparkline"))
