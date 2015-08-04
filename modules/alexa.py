import logging
import json
from idiotic import dispatcher, event, items, scenes

MODULE_NAME = "alexa"
VERSION = "1"

BASE_RESPONSE = {
    "version": VERSION,
    "response": {}
}

LOG = logging.getLogger("module.alexa")

def configure(config, api, assets):
    api.serve(test, '/', get_data=True, methods=['GET', 'POST', 'PUT', 'HEAD'], raw_result=True)

def test(data=None, *args, **kwargs):
    if data:
        data = json.loads(data.decode('UTF-8'))
    else:
        raise ValueError("Invalid arguments; no data")

    with open('/tmp/idiotic_test', 'a+') as f:
        f.write("Data  : " + json.dumps(data, indent=2, separators=(',', ': ')) + '\n')

    request = data["request"]
    req_type = request["type"]
    if req_type == "LaunchRequest":
        resp = dict(BASE_RESPONSE)
        resp["response"] = {
            "shouldEndRequest": False
        }
        return resp
    elif req_type == "SessionEndedRequest":
        resp = dict(BASE_RESPONSE)
        resp["response"] = {
            "shouldEndRequest": True
        }
        return resp
    elif req_type == "IntentRequest":
        # TODO validate timestamp
        if "intent" in request:
            intent = request["intent"]
            name = intent['name']
            slots = intent['slots']

            if name == "SetSwitch":
                target = None
                command = None

                for slot in slots.values():
                    slot_name = slot["name"]
                    slot_val = slot.get("value", None)

                    if slot_name == "Item":
                        try:
                            target = items[slot_val]
                        except (TypeError, NameError):
                            resp = dict(BASE_RESPONSE)
                            resp["response"] = {
                                "outputSpeech": {
                                    "type": "PlainText",
                                    "text": "No item '{}' found".format(slot_val)
                                },
                                "shouldEndSession": False
                            }
                            LOG.debug(str(resp))
                            return resp
                    elif slot_name == "NewStatus":
                        command = slot_val

                if target and command:
                    target.command(command)
                    resp = dict(BASE_RESPONSE)
                    resp["response"] = {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "OK"
                        },
                        "shouldEndSession": True
                    }
                    return resp
                else:
                    resp = dict(BASE_RESPONSE)
                    resp["response"] = {
                        "reprompt": {
                            "outputSpeech": {
                                "type": "PlainText",
                                "text": "Item or command not found '{}'".format(slot_val)
                            }
                        },
                        "shouldEndSession": True
                    }
                    return resp
            elif name == "SceneChange":
                target = None
                command = None

                for slot in slots.values():
                    slot_name = slot["name"]
                    slot_val = slot.get("value", None)

                    if slot_name == "Scene":
                        try:
                            target = scenes[slot_val.lower().replace(' ', '')]
                        except (TypeError, NameError):
                            resp = dict(BASE_RESPONSE)
                            resp["response"] = {
                                "outputSpeech": {
                                    "type": "PlainText",
                                    "text": "No scene '{}' found".format(slot_val)
                                },
                                "shouldEndSession": False
                            }
                            LOG.debug(str(resp))
                            return resp
                    elif slot_name == "Action":
                        command = slot_val

                if target and command:
                    if command and command.lower() in ("enter", "start", "enable"):
                        target.enter()
                    elif command and command.lower() in ("exit", "stop", "disable", "leave"):
                        target.exit()

                    resp = dict(BASE_RESPONSE)
                    resp["response"] = {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": "Entering {}".format(str(target))
                        },
                        "shouldEndSession": True
                    }
                    return resp

    return {'args': repr(args), 'kwargs': repr(kwargs)}
