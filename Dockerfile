FROM python:3.9.2-alpine

RUN pip install ahab
RUN pip install pyyaml
RUN pip install discord-webhook
RUN pip install python-telegram-bot
RUN pip install slack-webhook

RUN mkdir /yaml
RUN mkdir /deathWatch

ADD main.py /deathWatch/
ADD configInit.py /deathWatch/
ADD containerData.py /deathWatch/
ADD containerEvent.py /deathWatch/
ADD util.py /deathWatch/
ADD discordNotify.py /deathWatch/
ADD telegramNotify.py /deathWatch/
ADD slackNotify.py /deathWatch/
ADD logoIcons.py /deathWatch/


WORKDIR /deathWatch/
CMD [ "python", "-u", "main.py" ]