"""network -- Ping a device to see if it is on the network
"""
from idiotic.timer import Timer
import subprocess
import logging
import asyncio
import time
import os

LOG = logging.getLogger("module.network")

MODULE_NAME = "network"

checks = []

def start():
    scheduler.every().second.do(_refresh)

def _refresh(now=False):
    ctime = int(time.time())
    for check in checks:
        if now or ((ctime % check['interval']) == 0):
            if check['action'] == 'ping':
                for host in check['hosts']:
                    with open(os.devnull, 'w') as FNULL:
                        process = yield from asyncio.create_subprocess_exec("/usr/bin/ping","-c", "3", "-i", "0.2", host, stdout=FNULL, stderr=subprocess.STDOUT)
                        _ = yield from process.communicate()
                        if process.returncode == 0:
                            check['item'].on()
                            break
                else:
                    check['item'].off()
            else:
                LOG.info("Unknown action {action}".format(action=action))

def bind_item(item, action="ping", hosts=["localhost"], interval=60):
    LOG.info("Binding {name} to ping".format(name=item.name))
    checks.append({
            "action": action,
            "hosts": hosts,
            "interval": interval,
            "item": item,
        },
    )
