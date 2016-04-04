"""network -- Ping a device to see if it is on the network
"""
from idiotic.timer import Timer
import logging
LOG = logging.getLogger("module.network")
import time
import os

MODULE_NAME = "network"

hosts = []
checkTimer = None

def _refresh(now=False):
    global checkTimer
    ctime = int(time.time())
    for host in hosts:
        if now or ((ctime % host['interval']) == 0):
            if host['action'] == 'ping':
                if os.system("ping -c 3 " + host['host']):
                    host['item'].off()
                else:
                    host['item'].on()
            else:
                LOG.info("Unknown action {action}".format(action=action))
    checkTimer.reschedule()

def bind_item(item, action="ping", host="localhost", interval=60):
    LOG.info("Binding {name} to ping".format(name=item.name))
    global checkTimer
    if not checkTimer:
        LOG.info("Starting network update timer")
        checkTimer = Timer(1, _refresh)
        _refresh(now=True)
    hosts.append({
            "action": action,
            "host": host,
            "interval": interval,
            "item": item,
        },
    )

