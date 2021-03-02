import yaml
import util
from os import path
from dataclasses import dataclass
import sys


@dataclass
class Config:
    tags: list
    inclusions: list
    exclusions: list
    exitCodes: set
    restartPolicyEnabled: bool
    restartPolicyCountNotify: int
    telegramChatId: str
    telegramToken: str
    discordUrl: str
    slackUrl: str


conf = Config(None, None, None, {1, 139}, False, None, None, None, None, None)


def printSetConfig(finalConf):
    resultStr = "The following config params were set:\n"
    if finalConf.tags is not None:
        resultStr += f"- tags = {conf.tags}\n"
    if finalConf.inclusions is not None:
        resultStr += f"- inclusions = {conf.inclusions}\n"
    if finalConf.exclusions is not None:
        resultStr += f"- exclusions = {conf.exclusions}\n"

    resultStr += f"- container_exit_codes = {conf.exitCodes}\n"
    resultStr += f"- container_restart_policy_enabled = {conf.restartPolicyEnabled}\n"

    if finalConf.restartPolicyCountNotify is not None and finalConf.restartPolicyEnabled is True:
        resultStr += f"- container_restart_policy_max_count_notify = {conf.restartPolicyCountNotify}\n"
    if finalConf.telegramToken is not None:
        resultStr += f"- telegram.token = {conf.telegramToken}\n"
    if finalConf.telegramChatId is not None:
        resultStr += f"- telegram.chat_id = {conf.telegramChatId}\n"
    if finalConf.discordUrl is not None:
        resultStr += f"- discord.url = {conf.discordUrl}\n"
    if finalConf.slackUrl is not None:
        resultStr += f"- slack.url = {conf.slackUrl}\n"

    print(resultStr)


def initConfig():
    try:
        if path.exists('/yaml/config.yml'):
            with open('/yaml/config.yml') as f:
                docs = yaml.load_all(f, Loader=yaml.FullLoader)

                for doc in docs:
                    for k, v in doc.items():
                        if k == "general_settings" and v is not None:
                            for sk, sv in v.items():
                                if sk == "tags":
                                    conf.tags = sv
                                if sk == "inclusions":
                                    tmpSet = set()
                                    for item in sv:
                                        tmpSet.add(util.safeCast(item, str))
                                    conf.inclusions = set(filter(None, tmpSet))
                                if sk == "exclusions":
                                    tmpSet = set()
                                    for item in sv:
                                        tmpSet.add(util.safeCast(item, str))
                                    conf.exclusions = set(filter(None, tmpSet))

                        # KONTEJNERI
                        if k == "container_settings":
                            for ck, cv in v.items():
                                if ck == "exit_codes" and cv is not None:
                                    tmpSet = set()
                                    for item in cv:
                                        tmpSet.add(util.safeCast(item, int, None))
                                    conf.exitCodes = set(filter(None, tmpSet))
                                if ck == "restart_policy" and cv is not None:
                                    for resKey, resVal in cv.items():
                                        if resKey == "enabled":
                                            conf.restartPolicyEnabled = util.safeCastBool(resVal, False)
                                        if resKey == "max_count_notify":
                                            conf.restartPolicyCountNotify = util.safeCast(resVal, int, None)

                        # INNTEGRACIIII
                        if k == "integrations":
                            for intKey, intVal in v.items():
                                if intKey == "telegram" and intVal is not None:
                                    for telKey, telVal in intVal.items():
                                        if telKey == "token":
                                            conf.telegramToken = telVal
                                        if telKey == "chat_id":
                                            conf.telegramChatId = util.safeCast(telVal, int, None)

                                if intKey == "discord" and intVal is not None:
                                    for disKey, disVal in intVal.items():
                                        if disKey == "url":
                                            conf.discordUrl = disVal

                                if intKey == "slack" and intVal is not None:
                                    for disKey, disVal in intVal.items():
                                        if disKey == "url":
                                            conf.slackUrl = disVal

            # default to 5 count notify if the restart policy has been enabled and notify hasn't been set
            if conf.restartPolicyEnabled is True and conf.restartPolicyCountNotify is None:
                conf.restartPolicyCountNotify = 5

            # if the integrations are left on their default value - set them to None
            if conf.slackUrl == "<PASTE YOUR SLACK WEBHOOK HERE>":
                conf.slackUrl = None
            if conf.discordUrl == "<PASTE YOUR DISCORD WEBHOOK HERE>":
                conf.discordUrl = None
            if conf.telegramToken == "<PASTE YOUR TELEGRAM BOT TOKEN HERE>":
                conf.telegramToken = None
                conf.telegramChatId = None
            if conf.telegramChatId == "<PASTE YOUR TELEGRAM BOT CHAT_ID HERE>":
                conf.telegramChatId = None
                conf.telegramToken = None

            if conf.telegramToken is None and conf.telegramChatId is None and conf.discordUrl is None and conf.slackUrl is None:
                print("ERROR: At least one integration has to be set - now exiting!")
                sys.exit(0)
            elif (conf.telegramToken is not None and conf.telegramChatId is None) or (
                    conf.telegramToken is None and conf.telegramChatId is not None):
                print("ERROR: When using Telegram, both token and chat id must be set - now exiting!")
                sys.exit(0)

            printSetConfig(conf)
            return conf

        else:
            print(
                "ERROR: config.yml file not found (please bind the volume that contains the config.yml file) - now exiting!")
            sys.exit(0)

    except Exception as e:
        print("ERROR: config.yml file is not a valid yml file - now exiting!", e)
        sys.exit(0)
