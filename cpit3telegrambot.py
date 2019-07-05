import requests
import time
import schedule
from telegram.ext import Updater, CommandHandler
import os
import threading

TOKEN = os.getenv("TOKEN")
GROUPID = os.getenv("GROUPID")
WEBHOOK = os.getenv("WEBHOOK")
MESSAGE = os.getenv("MESSAGE")
PORT = int(os.environ.get('PORT', '8443'))
SCHEDULED_MESSAGE = os.getenv("SCHEDULED_MESSAGE")
TRIGGER_TIME = os.getenv("TRIGGER_TIME")
ENABLE_GM = os.getenv("ENABLE_GM")
QUESTIONS = os.getenv("QUESTIONS")
ANSWERS = os.getenv("ANSWERS")
DESCRIPTIONS = os.getenv("DESCRIPTIONS")
dictQuestionsAnwers = {'bagni': [MESSAGE, "Ci sono i bagni?"]}


def faq(bot, update):
    fullMessage = ""
    for key, val in dictQuestionsAnwers.items():
        fullMessage += "/" + key + " - " + val[1] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=fullMessage)


def bagni(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=MESSAGE)



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Benvenuto/a nel Bot del Campus Party Italia 3 \nCon il comando /faq potrai visualizzare tutte le domande ")


def sendGoodMorning():
    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + GROUPID + '&parse_mode=Markdown&text=' + SCHEDULED_MESSAGE
    response = requests.get(send_text)
    return response.json()


def loopGoodMorning():
    schedule.every().day.at(TRIGGER_TIME).do(sendGoodMorning)
    while True:
        schedule.run_pending()
        time.sleep(1)


if ENABLE_GM == "y":
    t = threading.Thread(target=loopGoodMorning)
    t.daemon = True
    t.start()

while True:
    updater = Updater(TOKEN)
    answersList = ANSWERS.split(sep="|")
    questionsList = QUESTIONS.split(sep="|")
    descriptionList = DESCRIPTIONS.split(sep="|")
    for idx, val in enumerate(questionsList):
        dictQuestionsAnwers[val] = [answersList[idx], descriptionList[idx]]
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bagni', bagni))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('faq', faq))
    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(WEBHOOK + TOKEN)
    updater.idle()
