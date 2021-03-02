import configInit
import containerEvent
import containerData
from datetime import datetime
from ahab import Ahab
import discordNotify
import telegramNotify
import slackNotify


if __name__ == '__main__':
    print("STARTING SCRIPT!")

    config = configInit.initConfig()

    def mainProcess(event, data):
        # all containers will be listened for
        if config.inclusions is None and config.exclusions is None:
            manageIntegrations(event, data)
        # only the following containers will be excluded
        elif config.inclusions is None and config.exclusions is not None:
            if event.name not in config.exclusions:
                manageIntegrations(event, data)
        # only the following containers will be listened for
        elif config.inclusions is not None and config.exclusions is None:
            if event.name in config.inclusions:
                manageIntegrations(event, data)
        # only the following containers will be lisened for, minus all the ones in the exclusion list
        elif config.inclusions is not None and config.exclusions is not None:
            resSet = list(config.inclusions - config.exclusions)
            if event.name in resSet:
                manageIntegrations(event, data)

    def manageIntegrations(event, data):
        if config.discordUrl is not None:
            discordNotify.sendDiscordMsg(event, data, config)
        if config.telegramToken is not None and config.telegramChatId is not None:
            telegramNotify.sendTelegramMsg(event, data, config)
        if config.slackUrl is not None:
            slackNotify.sendSlackNotify(event, data, config)

    def processRestartPolicy(event, data):
        if config.restartPolicyEnabled:
            if event is not None and data is not None and containerEvent.checkIfEventDie(event) and \
                    event.exitCode in config.exitCodes and data.exitCode in config.exitCodes:
                mainProcess(event, data)
            elif data is not None and data.status == "restarting":
                mainProcess(event, data)
        elif event is not None and data is not None and containerEvent.checkIfEventDie(event) and event.exitCode in \
                config.exitCodes and data.exitCode in config.exitCodes:
            mainProcess(event, data)

    def f(rawEvent, rawData):
        event = containerEvent.getEvent(rawEvent)
        data = containerData.getData(rawData, config)

        processRestartPolicy(event, data)


    listener = Ahab(handlers=[f])
    listener.listen()
