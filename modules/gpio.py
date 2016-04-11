import sys
import time
import functools
import RPi.GPIO as gpio

SETUP_PINS = set()

def convert_state(state):
    if state in ("low", "off") or not state:
        return gpio.LOW

    if state in ("high", "on"):
        return gpio.HIGH

def convert_pull(state):
    if state in ("down", "low"):
        return gpio.PUD_DOWN
    elif state in ("up", "high"):
        return gpio.PUD_UP
    else:
        return gpio.PUD_NONE

def convert_edge(state):
    if state in ("rising", "rise"):
        return gpio.RISING
    elif state in ("falling", "fall"):
        return gpio.FALLING
    else:
        return gpio.BOTH

def output_high(pin):
    if check_setup(pin):
        gpio.output(pin, gpio.HIGH)

def output_low(pin):
    if check_setup(pin):
        gpio.output(pin, gpio.LOW)

def read(pin):
    if check_setup(pin):
        return bool(gpio.read(pin))

def check_setup(pin):
    if pin in SETUP_PINS:
        return True
    raise ValueError("GPIO pin {} is not set up.".format(pin))

def configure(config, api, assets):
    mode = config.get("mode", "bcm")

    if mode == "bcm":
        gpio.setmode(gpio.BCM)
    elif mode == "board":
        gpio.setode(gpio.BOARD)

    api.serve(output_high, '/output/<pin>/high')
    api.serve(output_low, '/output/<pin>/low')
    api.serve(read, '/input/<pin>')

def bind_item(item, **config):
    if "input" in config:
        bind_input(item, config["input"])

    if "output" in config:
        bind_output(item, config["output"])

    if "pwm" in config:
        bind_pwm(item, config["pwm"])

def state_callback(item, pin, mapping, edge):
    if edge == gpio.BOTH:
        state = gpio.input(pin)
    elif edge == gpio.RISING:
        state = gpio.HIGH
    elif edge == gpio.FALLING:
        state == gpio.LOW

    item.state = mapping.get("high" if state == gpio.HIGH else "low")

def command_callback(item, pin, mapping, edge):
    if edge == gpio.BOTH:
        state = gpio.input(pin)
    elif edge == gpio.RISING:
        state = gpio.HIGH
    elif edge == gpio.FALLING:
        state == gpio.LOW

    item.command(mapping.get("high" if state == gpio.HIGH else "low"))

def bind_input(item, config):
    try:
        pin = config["pin"]

        pud = convert_pull(config.get("pull", None))
        edge = convert_edge(config.get("edge", None))
        debounce = config.get("debounce", None)

        gpio.setup(pin, gpio.IN, pull_up_down=pud)
        SETUP_PINS.add(pin)

        if "state" in config:
            GPIO.add_event_detect(pin, edge, bouncetime=debounce,
                                  callback=functools.partial(
                                      state_callback, item, pin,
                                      config["state"], edge))

        if "command" in config:
            GPIO.add_event_detect(pin, edge, bouncetime=debounce,
                                  callback=functools.partial(
                                      command_callback, item, pin,
                                      config["command"], edge))
    except TypeError:
        for part in config:
            bind_input(item, part)

def state_binder(item, pin, config, evt):
    if "mapping" in config:
        out = config["mapping"].get(evt.new)
    elif "function" in config:
        out = config["function"](evt.new)

    kind = config.get("kind", "constant")
    delay = config.get("delay", 100)

    do_output(item, pin, out, kind, delay, evt)

def command_binder(item, pin, config, evt):
    if "mapping" in config:
        out = config["mapping"].get(evt.command)
    elif "function" in config:
        out = config["function"](evt.command)

    kind = config.get("kind", "constant")
    delay = config.get("delay", 100)

    do_output(item, pin, out, kind, delay, evt)

def do_output(item, pin, state, kind, delay, evt):
    if kind == "constant":
        gpio.output(pin, convert_state(out))        
    elif kind == "button_high":
        # The button is active when high
        # Default low, and swap to high for {delay} to trigger
        gpio.output(pin, gpio.HIGH)
        time.sleep(delay)
        gpio.output(pin, gpio.LOW)
    elif kind == "button_low":
        # The button is active when low
        # Default high, and swap to low for {delay} to trigger
        gpio.output(pin, gpio.LOW)
        time.sleep(delay)
        gpio.output(pin, gpio.HIGH)
    else:
        raise ValueError("Unknown output kind '{}' for GPIO binding".format(kind))

def bind_output(item, config):
    try:
        pin = config["pin"]

        default = convert_state(item.get("default", "low"))

        gpio.setup(pin, gpio.OUT, default)
        SETUP_PINS.add(pin)

        if default is not None:
            gpio.output(pin, default)

        if "state" in config:
            item.bind_on_change(functools.partial(state_binder, pin, config["state"]), kind="after")

        if "command" in config:
            item.bind_on_command(functools.partial(command_binder, pin, config["command"]), kind="after")
    except TypeError:
        for part in config:
            bind_output(item, part)

def bind_pwm(item, config):
    raise NotImplementedError("PWM outputs are not implemented, sorry!"
