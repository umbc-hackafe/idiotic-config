from idiotic.item import Toggle, Trigger, Number, Group

people = [("Dylan", ["dylanphone",]),
          ("Mark", ["markphone",]),
          ("Sasha", ["sashaphone",])]

for name, devices in people:
    Toggle(name + " Presence",
           bindings={"network": {"action": "ping",
                                 "hosts": devices,
                                 "interval": 60}},
           tags=("presence", "presence_" + name.lower()))
