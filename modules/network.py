"""network -- Ping a device to see if it is on the network
"""
from idiotic.timer import Timer
import logging
import subprocess
import time
import os

LOG = logging.getLogger("module.network")

MODULE_NAME = "network"

checks = []
checkTimer = None

def _refresh(now=False):
    global checkTimer
    ctime = int(time.time())
    for check in checks:
        if now or ((ctime % check['interval']) == 0):
            if check['action'] == 'ping':
                for host in check['hosts']:
                    with open(os.devnull, 'w') as FNULL:
                        if not subprocess.call(["ping", "-c", "3", host], stdout=FNULL, stderr=subprocess.STDOUT):
                            check['item'].on()
                            break
                else:
                    check['item'].off()
            else:
                LOG.info("Unknown action {action}".format(action=action))
    checkTimer.reschedule()

def bind_item(item, action="ping", hosts=["localhost"], interval=60):
    LOG.info("Binding {name} to ping".format(name=item.name))
    checks.append({
            "action": action,
            "hosts": hosts,
            "interval": interval,
            "item": item,
        },
    )

    global checkTimer
    if not checkTimer:
        LOG.info("Starting network update timer")
        checkTimer = Timer(1, _refresh)
        _refresh(now=True)