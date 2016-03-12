from idiotic.item import Toggle, Trigger, Number, Group

people = [("Dylan", "dylan-gs5"),
          ("Mark", "tsubasa"),
          ("Noah", "noah-laptop"),
          ("Sasha", "sasha-phone")]

for name, device in people:
    Toggle(name + " Presence",
           bindings={"network": {"action": "ping",
                                 "host": device,
                                 "interval": 60}},
           tags=("presence", "presence_" + name.lower()))
