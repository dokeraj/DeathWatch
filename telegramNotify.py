import containerEvent as eventData
import containerData as dataData
import configInit
import telegram
import sys


def sendTelegramMsg(event: eventData.ContEvent, data: dataData.ContData, config: configInit.Config):
    bot = telegram.Bot(token=config.telegramToken)

    aggMsg = f"Docker Container `{event.name.capitalize()}` *Crashed*\n\n"

    fixErrorMsg = str(data.errorMsg).replace("¯\_(ツ)_/¯", "")

    tagsField = ""
    if config.tags is not None:
        tags = ""
        for t in config.tags:
            tags = tags + f"`{t}`; "

        tagsField = f"🚩 *Tags*\n{tags}\n\n"

    aggMsg += tagsField

    restartPolicy = ""
    if data.restartPolicy is not None:
        restartPolicy = f"🔁 *Restart Policy*: `{data.restartPolicy}`\n🔂 *Max Count Restarts Notify*: `{config.restartPolicyCountNotify}`\n"
        restartPolicy = restartPolicy + f"🔄 *Current Restart Count*: `{data.restartCount}`\n\n"
    aggMsg += restartPolicy

    image = f"🖼️ *Image*\n`{event.image}`\n\n"
    aggMsg += image

    exitCode = f"🔸 *Exit Code*\n `{data.exitCode}`\n\n"
    aggMsg += exitCode

    oomKilled = f"💢 OOMKilled\n`{data.oomKilled}`\n\n"
    aggMsg += oomKilled

    finalMsg = aggMsg + fixErrorMsg
    finalMsgFixed = finalMsg.replace(".", "\.").replace("(", "\(").replace(")", "\)").replace("!", "\!").replace(",", "\,").replace("-", "\-").replace("=", "\=").replace("+", "\+").replace("#", "\#").replace(">", "\>").replace("<", "\<").replace("|", "\|")

    try:
        bot.sendMessage(chat_id=config.telegramChatId, text=finalMsgFixed, parse_mode='MarkdownV2')
    except Exception as e:
        print(f"ERROR while sending message to Telegram. Please check if the chatID and token are valid - now exiting! {e}")
        sys.exit(0)
