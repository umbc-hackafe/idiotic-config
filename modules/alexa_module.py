import logging
import pyalexa
import itertools

MODULE_NAME = "alexa"
VERSION = "2"

SKILL = None

SCENE_ENTER_COMMANDS = ("enter", "start", "enable")
SCENE_EXIT_COMMANDS = ("exit", "stop", "disable", "leave")

def configure(config, api, assets):
    global SKILL
    SKILL = pyalexa.Skill(app_id=config["app_id"])

    api.serve(SKILL.flask_target, '/', methods=['POST', 'GET'], raw_result=True,
              no_source=True, content_type="application/json")
    api.serve(generate_utterances, '/utterances', raw_result=True, no_source=True, content_type="text/plain")

    @SKILL.launch
    def launch(request):
        return request.response(end=False)

    @SKILL.end
    def end(request):
        return request.response(end=True)

    @SKILL.intent("GetState")
    def get_state(request):
        if not request.data().get("Item"):
            return request.response(end=False, speech="Please specify an item")

        name = request.data().get("Item")

        try:
            target = items[name]
            return request.response(end=True, speech="{} is: {}".format(target.name, target.state))
        except NameError:
            return request.response(end=False, speech="Item {} not found.".format(name))
        except AttributeError:
            return request.response(end=True, speech="{} does not have a state.".format(target.name))

    @SKILL.intent("SetState")
    def get_state(request):
        if not request.data().get("Item"):
            return request.response(end=False, speech="Please specify an item")

        if not request.data().get("NewState"):
            return request.response(end=False, speech="Please specify a state")

        name = request.data().get("Item")
        state = request.data().get("NewState")

        try:
            target = items[name]

            target.state = state
            return request.response(end=True, speech="{} is now {}.".format(target.name, target.state))
        except NameError:
            return request.response(end=False, speech="Item {} not found.".format(name))
        except:
            return request.response(end=True, speech="Invalid state {}.".format(state))

    @SKILL.intent("SetSwitch")
    def set_switch(request):
        if not request.data().get("Item"):
            return request.response(end=False, speech="Please specify an item")

        if not request.data().get("NewStatus"):
            return request.response(end=False, speech="Please specify a command")

        name = request.data().get("Item")
        command = request.data().get("NewStatus")

        try:
            target = items[name]
            target.command(command)
            return request.response(end=True, speech="Okay.")
        except NameError:
            return request.response(end=False, speech="Item {} not found.".format(name))
        except AttributeError:
            return request.response(end=False, speech="Item {} has no command {}".format(name, command))

    @SKILL.intent("SceneChange")
    def scene_change(request):
        if not request.data().get("Scene"):
            return request.response(end=False, speech="Please specify a scene.")

        if not request.data().get("Action"):
            return request.response(end=False, speech="Please specify 'enter' or 'exit'")

        name = request.data().get("Scene")
        action = request.data().get("Action").lower()

        try:
            scene = scenes[name]
            if action in SCENE_ENTER_COMMANDS:
                scene.enter()
                return request.response(end=True, speech="Entering scene {}".format(name))
            elif action in SCENE_EXIT_COMMANDS:
                scene.exit()
                return request.response(end=True, speech="Exiting scene {}".format(name))
        except NameError:
            return request.response("Scene '{}' not found".format(name))

UTTERANCES = [
    (
        "GetState", [
            ("Item", lambda: items.all())
        ], [
            "about the {{{0.name}|Item}}",
            "about {{{0.name}|Item}}",
            "what is the {{{0.name}|Item}}",
            "what the {{{0.name}|Item}} is",
            "what state the {{{0.name}|Item}} is",
            "what state the {{{0.name}|Item}} is in",
            "what state is the {{{0.name}|Item}} in",
            "what state is the {{{0.name}|Item}} in",
        ]
    ),(
        "SetSwitch",
        [
            ("Item", lambda: items.all()),
            ("NewStatus", lambda i: list(i.commands().keys()) + list(i.aliases.keys()))
        ], [
            "Turn {{{0.name}|Item}} {{{1}|NewStatus}}",
            "Turn {{{0.name}|Item}} to {{{1}|NewStatus}}",
            "Turn the {{{0.name}|Item}} {{{1}|NewStatus}}",
            "Turn the {{{0.name}|Item}} to {{{1}|NewStatus}}",
            "Turn {{{1}|NewStatus}} {{{0.name}|Item}}",
            "Turn {{{1}|NewStatus}} the {{{0.name}|Item}}",
            "Set {{{0.name}|Item}} {{{1}|NewStatus}}",
            "Set {{{0.name}|Item}} to {{{1}|NewStatus}}",
            "Set the {{{0.name}|Item}} {{{1}|NewStatus}}",
            "Set the {{{0.name}|Item}} to {{{1}|NewStatus}}",
            "Set {{{1}|NewStatus}} {{{0.name}|Item}}",
            "Set {{{1}|NewStatus}} the {{{0.name}|Item}}",
            "{{{1}|NewStatus}} the {{{0.name}|Item}}",
            "{{{1}|NewStatus}} {{{0.name}|Item}}",
        ]
    ),(
        "SceneChange",
        [
            ("Scene", lambda: scenes.all()),
            ("Action", lambda _: SCENE_ENTER_COMMANDS + SCENE_EXIT_COMMANDS)
        ], [
            "{{{1}|Action}} {{{0.name}|Scene}}",
            "{{{1}|Action}} the {{{0.name}|Scene}}",
            "{{{1}|Action}} the {{{0.name}|Scene}} scene",
            "{{{1}|Action}} the scene {{{0.name}|Scene}}",
            "{{{1}|Action}} scene {{{0.name}|Scene}}",
        ]
    ),
]

def __product(*args):
    return itertools.product(*(arg if isinstance(arg, (list,tuple)) else [arg] for arg in args))

def __parse_utterance(name, slots, phrases, items=[]):
    if not slots:
        return [name + " " + phrase.format(*slotvals)
                for phrase in phrases
                for item in items
                for slotvals in __product(*item)]

    slot_name, item_lambda = slots[0]
    slots = slots[1:]

    if items:
        for i, v in enumerate(items):
            items[i] = v + (item_lambda(*v),)
    else:
        items = list(zip(item_lambda()))

    return __parse_utterance(name, slots, phrases, items)

def generate_utterances():
    return '\n'.join(('\n'.join(__parse_utterance(*utterance)) for utterance in UTTERANCES))
