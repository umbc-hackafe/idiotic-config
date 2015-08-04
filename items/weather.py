from idiotic.item import Toggle, Trigger, Number, Group
from idiotic import modules, scheduler

Number("Brightness",
       bindings={"http": {"pull": "luna:8081/lx"}},
       tags=("weather", "climate", "webui.show_sparkline"))
