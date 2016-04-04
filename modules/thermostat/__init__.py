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
        if not self.enabled:
            for i in self.heaters:
                i.off()
            for i in self.chillers:
                i.off()
            return
            
        if not type(self.state) is float:
            self.state = 23
        for i in self.temps.keys():
            vals = i.state_history.last(self.memory)
            if len(vals) > 0:
                break
        if not vals:
            LOG.info("No temperature data available!")
            return
        history = []
        for val in vals:
            sum = 0
            length = len(self.temps)
            for temp in self.temps:
                closest = temp.state_history.closest(val.time)
                weight = self.weights[self.name+"-temp-"+temp.name].state
                if closest:
                    if type(closest.state) is float:
                        if closest.state:
                            sum += closest.state*weight
                        else:
                            length += -1
                            LOG.info("State was zero. Not likely, but possible.")
                    else:
                        length += -1
                        LOG.info("State was not a float. What?!?")
                else:
                    length += -1
                    LOG.info("No history found for {name}".format(name=temp.name))
            if length > 0:
                history.append({'time':float(val.time.timestamp()), 'temp':float(sum/length)})
            else:
                LOG.info("Not enough temperature data to make a decision")
                for i in self.heaters:
                    i.off()
                for i in self.chillers:
                    i.off()
                return                
        for i in self.temps:
            LOG.debug("{name}: {last}".format(name=i.name, last=i.state_history.last()))
        if self.algorithm == "pid":
            chill, heat = pid(history, self.state, self.variance)
        elif self.algorithm == "pd":
            chill, heat = pd(history, self.state, self.variance)
        else:
            chill, heat = simple(history, self.state, self.variance)
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
        self.state = val
        self.update()
