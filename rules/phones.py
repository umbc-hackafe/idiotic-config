from idiotic.rule import bind, Event
from idiotic.timer import Timer
from idiotic import instance as c

@bind(Event(type=c.modules.sms.SMSReceivedEvent))
def on_sms(evt):
    items.alert_beacon.on()
    modules.sign.new_message("{} - {}".format(evt.body, evt.sender),
                             effects=['scroll'], priority=10, lifetime=45)
    Timer(30, items.alert_beacon.off).start()
