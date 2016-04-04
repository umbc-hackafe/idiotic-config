"""Intelligent controls for temperature
"""
import logging
from idiotic.item import BaseItem, command, Number
from .controls import *

MODULE_NAME = "thermostat"

LOG = logging.getLogger("module.thermostat")

class Thermostat(BaseItem):
    def __init__(self, *args, chillers=[], heaters=[], temps={}, humidities={}, algorithm="pid", memory=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.chillers = chillers
        self.heaters = heaters
        self.temps = temps
        self.humidities = humidities
        self.setpoint = Number(self.name+"-setpoint")
        self.variance = 1
        self.algorithm = algorithm
        self.memory = memory
        self.weights = {}

        for temp in self.temps.keys():
            temp.bind_on_change(self.update, kind="after")
            self.weights[self.name+"-temp-"+temp.name] = Number(self.name+"-temp-"+temp.name)
            self.weights[self.name+"-temp-"+temp.name].state = self.temps[temp]
        for humid in self.humidities.keys():
            humid.bind_on_change(self.update, kind="after")
            self.weights[self.name+"-humid-"+humid.name] = Number(self.name+"-humid-"+humid.name)
            self.weights[self.name+"-humid-"+humid.name].state = self.humidities[humid]

    def update(self, evt=None):
        if self.setpoint.state is None:
            self.setpoint.state = 25
        vals = list(self.temps.keys())[0].state_history.last(self.memory)
        history = []
        for val in vals:
            sum = 0
            for temp in self.temps:
                sum += temp.state_history.closest(val.time).state*self.weights[self.name+"-temp-"+temp.name].state
            history.append({'time':float(val.time.timestamp()), 'temp':float(sum)})
        if self.algorithm == "pid":
            chill, heat = pid(history, self.setpoint.state, self.variance)
        elif self.algorithm == "pd":
            chill, heat = pd(history, self.setpoint.state, self.variance)
        else:
            chill, heat = simple(history, self.setpoint.state, self.variance)
        LOG.debug("AC set to {ac} and heat set to {heat}".format(ac=chill, heat=heat))
        for i in self.heaters:
            if heat:
                i.on()
            else:
                i.off()
        for i in self.chillers:
            if chill:
                i.on()
            else:
                i.off()
                
        if evt:
            LOG.debug("Updated: {item} to {state}".format(item=evt.item.name, state=evt.new))

    @command
    def set(self, val: float):
        self.setpoint.state = val
        self.update()
