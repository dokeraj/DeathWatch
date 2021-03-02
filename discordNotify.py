from discord_webhook import DiscordWebhook, DiscordEmbed
import containerEvent as eventData
import containerData as dataData
import configInit
import sys
import logoIcons


def sendDiscordMsg(event: eventData.ContEvent, data: dataData.ContData, config: configInit.Config):
    webhook = DiscordWebhook(url=config.discordUrl)

    tagsField = ""
    if config.tags is not None:
        tags = ""
        for t in config.tags:
            tags = tags + f"*{t}*; "

        tagsField = f":flags: ** Tags **\n{tags}\n\n"

    embedColor = 13701670
    authorName = "Docker Container Crashed!"
    authorIcon = logoIcons.getLogoUrl(event.image)

    embedDescRestartPolicy = ""
    if data.restartPolicy is not None:
        embedDescRestartPolicy = f":repeat: **Restart Policy**: *{data.restartPolicy}*\n:repeat_one: **Max Count Restarts Notify**: *{config.restartPolicyCountNotify}*"

    embedDesc = f"{data.errorMsg}\n\n{tagsField}{embedDescRestartPolicy}"

    embed = DiscordEmbed(title=f":pirate_flag: {event.name.capitalize()}", description=embedDesc, color=embedColor)
    embed.set_author(name=authorName, icon_url=authorIcon)

    embed.add_embed_field(name=":frame_photo: Image", value=event.image, inline=True)
    embed.add_embed_field(name=":anger: OOMKilled", value=str(data.oomKilled), inline=True)
    embed.add_embed_field(name=":small_orange_diamond: Exit Code", value=str(data.exitCode), inline=True)

    if data.restartPolicy is not None:
        embed.add_embed_field(name=":arrows_counterclockwise: Current Restart Count", value=str(data.restartCount),
                              inline=True)

    webhook.add_embed(embed)
    try:
        webhook.execute()
    except Exception as e:
        print("ERROR: discord Url is not valid - now exiting!")
        sys.exit(0)
