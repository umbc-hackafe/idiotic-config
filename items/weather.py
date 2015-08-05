from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Number("Brightness",
       bindings={"http": {"pull": (30, "luna:8081/lx", None, float)}},
       tags=("weather", "climate", "webui.show_sparkline"))
