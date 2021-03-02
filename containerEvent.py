from dataclasses import dataclass
import util

@dataclass
class ContEvent:
    status: str
    type: str
    action: str
    image: str
    exitCode: int
    name: str


def getEvent(ev):
    event = ContEvent(None, None, None, None, None, None)

    if "status" in ev:
        event.status = ev["status"]

    event.type = ev["Type"]
    event.action = ev["Action"]

    try:
        event.image = ev["Actor"]["Attributes"]["image"]
        event.exitCode = int(ev["Actor"]["Attributes"]["exitCode"])
    except KeyError:
        pass

    event.name = util.safeCast(ev["Actor"]["Attributes"]["name"], str)

    if event.type == "container":
        return event

    return None


def checkIfEventDie(event):
    return event.action == "die" or event.status == "die" or event.action == "oom" or event.status == "oom"

