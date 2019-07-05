import requests
import time
import schedule
from telegram.ext import Updater, CommandHandler
import os
import threading

TOKEN = os.getenv("TOKEN")
GROUPID = os.getenv("GROUPID")
updater = Updater(TOKEN)
WEBHOOK = os.getenv("WEBHOOK")
MESSAGE = os.getenv("MESSAGE")
PORT = int(os.environ.get('PORT', '8443'))
SCHEDULED_MESSAGE = os.getenv("SCHEDULED_MESSAGE")
TRIGGER_TIME = os.getenv("TRIGGER_TIME")
ENABLE_GM = os.getenv("ENABLE_GM")
QUESTIONS = os.getenv("QUESTIONS")
ANSWERS = os.getenv("ANSWERS")
DESCRIPTIONS = os.getenv("DESCRIPTIONS")
dictQuestionsAnwers = {'bagni': [MESSAGE,"Ci sono i bagni?"]}


def faq(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    for key,val in dictQuestionsAnwers.items():
        bot.send_message(chat_id=chat_id, text="/"+ key +" - "+ val[1] )


def bagni(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    bot.send_message(chat_id=chat_id, text=MESSAGE)


def sendGoodMorning():
    bot_chatID = GROUPID
    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + SCHEDULED_MESSAGE
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
    answersList = ANSWERS.split(sep="|")
    questionsList = QUESTIONS.split(sep="|")
    descriptionList = DESCRIPTIONS.split(sep="|")
    for idx, val in enumerate(questionsList):
        dictQuestionsAnwers[val] = [answersList[idx],descriptionList[idx]]
    print(dictQuestionsAnwers)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bagni', bagni))
    dp.add_handler(CommandHandler('faq', faq))
    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(WEBHOOK + TOKEN)
    updater.idle()
