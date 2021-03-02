from slack_webhook import Slack
import containerEvent as eventData
import containerData as dataData
import configInit
import sys
import logoIcons


def newSection(text, imageUrl=None):
    mainPart = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }

    return mainPart


def divider():
    return {
        "type": "divider"
    }


def sectionWithImage(text, imageUrl):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": {
            "type": "image",
            "image_url": imageUrl,
            "alt_text": "image icon"
        }
    }


def sendSlackNotify(event: eventData.ContEvent, data: dataData.ContData, config: configInit.Config):
    slackClient = Slack(url=config.slackUrl)

    imageIcon = logoIcons.getLogoUrl(event.image)
    mainInfo = f"_Docker Container Crashed Detected_\n\n:pirate_flag: *Container Name*\n `{event.name.capitalize()}`\n\n"
    introMsg = sectionWithImage(mainInfo, imageIcon)

    errorMsg = newSection(f"{data.errorMsg}\n")

    tagsField = None
    if config.tags is not None:
        tags = ""
        for t in config.tags:
            tags = tags + f"`{t}`; "

        tagsField = f":flags: *Tags*\n{tags}\n\n"
        tagsField = newSection(tagsField)

    restartPolicy = None
    if data.restartPolicy is not None:
        restartPolicy = f":repeat: *Restart Policy*: `{data.restartPolicy}`\n:repeat_one: *Max Count Restarts Notify*: `{config.restartPolicyCountNotify}`\n"
        restartPolicy = restartPolicy + f":arrows_counterclockwise: *Current Restart Count*: `{data.restartCount}`\n\n"
        restartPolicy = newSection(restartPolicy)

    image = f":frame_with_picture: *Image*\n`{event.image}`\n\n"
    image = newSection(image)

    exitCode = f":small_orange_diamond: *Exit Code*\n `{data.exitCode}`\n\n"
    exitCode = newSection(exitCode)

    oomKilled = f":anger: OOMKilled\n`{data.oomKilled}`\n\n"
    oomKilled = newSection(oomKilled)

    allFields = [introMsg, errorMsg, divider(), tagsField, restartPolicy, image, exitCode, oomKilled]

    filteredFields = [i for i in allFields if i]

    try:
        slackClient.post(blocks=filteredFields)
    except Exception as e:
        print(f"ERROR while sending message to Slack. Please check if the webhook URL is valid - now exiting! {e}")
        sys.exit(0)
