from dataclasses import dataclass
import configInit


@dataclass
class ContData:
    status: str
    exitCode: int
    oomKilled: str
    errorMsg: str
    restartCount: int
    restartPolicy: str


def getData(rawData, conf: configInit.Config):
    contData = ContData(None, None, None, None, None, None)

    try:
        contData.status = rawData["State"]["Status"]
        contData.oomKilled = rawData["State"]["OOMKilled"]
        contData.exitCode = int(rawData["State"]["ExitCode"])

        contData.errorMsg = rawData["State"]["Error"]
        if contData.errorMsg == "":
            contData.errorMsg = """Please check container logs for more info.. ¯\_(ツ)_/¯"""

        contData.restartPolicy = rawData["HostConfig"]["RestartPolicy"]["Name"]
        if contData.restartPolicy == "":
            contData.restartPolicy = None

        contData.restartCount = rawData["RestartCount"]

    except KeyError:
        pass

    if contData.oomKilled is True or contData.status == "exited" or (
            conf.restartPolicyEnabled and contData.status == "restarting" and contData.restartCount <= conf.restartPolicyCountNotify):
        return contData

    return None
