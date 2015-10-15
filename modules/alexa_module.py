import logging
import pyalexa
from idiotic import dispatcher, event, items, scenes

MODULE_NAME = "alexa"
VERSION = "2"

SKILL = None

def configure(config, api, assets):
    global SKILL
    SKILL = pyalexa.Skill(app_id=config["app_id"])

    api.serve(SKILL.flask_target, '/', methods=['POST', 'GET'], raw_result=True,
              no_source=True, content_type="application/json")


    @SKILL.launch
    def launch(request):
        return request.response(end=False)

    @SKILL.end
    def end(request):
        return request.response(end=True)

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

        name = request.data().get("Scene").lower().replace(' ', '')
        action = request.data().get("Action").lower()

        try:
            scene = scenes[name]
            if action in ("enter", "start", "enable"):
                scene.enter()
                return request.response(end=True, speech="Entering scene {}".format(name))
            elif action in ("exit", "stop", "disable"):
                scene.exit()
                return request.response(end=True, speech="Exiting scene {}".format(name))
        except NameError:
            return request.response("Scene '{}' not found".format(name))
