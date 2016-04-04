from idiotic.item import Toggle, Trigger, Number, Group

people = [("Dylan", ["dylanchromebook", "dylancell", ]),
          ("Mark", ["dom", "dom-wired", "markcell",]),
          ("Sasha", ["mosaic", "sashacell",]),
          ("Jerry", ["jerry", "jerryphone",]),
         ]

for name, devices in people:
    Toggle(name + " Presence",
           bindings={"network": {"action": "ping",
                                 "hosts": devices,
                                 "interval": 60}},
           tags=("presence", "presence_" + name.lower()))
