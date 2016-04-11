from idiotic.item import Toggle, Trigger, Number, Group, Text

Toggle("Switch",
       tags=("input",),
       bindings={"gpio": {"input": {
           "pin": 16,
           "edge": "both",
           "command": {
               "mapping": {"high": "on", "low": "off"}
           }
       }}})

Toggle("Buzzer",
       tags=("output",),
       bindings={"gpio": {"output": {
           "pin": 11,
           "default": "high",
           "command": {
               "mapping": {"on": "low", "off": "high"}
           }
       }}})

Toggle("LED",
       tags=("output",),
       bindings={"gpio": {"output": {
           "pin": 13,
           "default": "low",
           "command": {
               "mapping": {"on": "high", "off": "low"}
           }
       }}})

#Number("Dial",
#       bindings={"gpio": {"output": {
#           "type": "pwm",
#           "pin": 12,
#           "default": "low",
#           "state": {
#               "function": lambda n: max(min(1,n),0)
#           }
#       }}})
