#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram import error
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import requests
import logging
import redis
import os
import re
import json
from ulduz.constants import TELEGRAM_WORKER_QUEUE

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMAIL, PERIOD, REPO_COUNT, GITHUB, GITLAB = range(5)
ALLOWED_PERIODS = ["daily", "weekly", "monthly"]
try:
    TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

    # Expected: http://address_to_api/v#/Subscriptions/
    API_URL = os.environ['REST_API_URL']
except KeyError:
    logger.error("KeyError: Error while getting environment variables. Did you set them correctly?")
    exit(-1)

class Bot:
    def __init__(self, token):
        pattern = re.compile('^({})$'.format("|".join(ALLOWED_PERIODS)), flags=re.IGNORECASE)
        updater = Updater(token)
        self.updater = updater
        self.bot = updater.bot
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('subscribe', self.subscribe, pass_user_data=True)],

            states={
                EMAIL: [MessageHandler(Filters.text, self.email, pass_user_data=True),
                                ],

                PERIOD: [RegexHandler(pattern, self.period, pass_user_data=True),
                                ],
                REPO_COUNT: [MessageHandler(Filters.text, self.repo_count, pass_user_data=True)
                                ],

                GITHUB: [RegexHandler('^(([a-zA-Z]|\d|-|_)+|(, )+)+$', self.github, pass_user_data=True),
                        CommandHandler("skip", self.skip_github, pass_user_data=True),
                               ],

                GITLAB: [RegexHandler('^(([a-zA-Z]|\d|-|_)+|(, )+)+$', self.gitlab, pass_user_data=True),
                        CommandHandler("skip", self.skip_gitlab, pass_user_data=True),
                               ],
            },

            fallbacks=[CommandHandler('cancel', self.cancel, pass_user_data=True),
                        MessageHandler(Filters.text, self.wrong_answer, pass_user_data=True),
                           ]
        )

        dp.add_handler(conv_handler)
        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling(clean=True)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # updater.idle()


    def subscribe(self, bot, update, user_data):
        update.message.reply_text("Please send your email address:")
        user = update.message.from_user
        user_data["telegramID"] = user.id
        user_data["STATE"] = EMAIL
        return EMAIL

    def email(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send your message period preference (weekly, daily, monthly):")
        user_data["email"] = text
        user_data["STATE"] = PERIOD
        return PERIOD

    def period(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("How many repos would you like to get?")
        user_data["period"] = text
        user_data["STATE"] = REPO_COUNT
        return REPO_COUNT

    def repo_count(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send github ids you want to subscribe to by seperating them with a comma and space")
        update.message.reply_text("Or you can /skip")
        user_data["repoCount"] = text
        user_data["STATE"] = GITHUB
        return GITHUB

    def github(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send gitlab ids you want to subscribe to by seperating them with a comma and space")
        update.message.reply_text("Or you can /skip")
        user_data["subscriptions"] = {}
        user_data["subscriptions"]["github"] = text.split(", ")
        user_data["STATE"] = GITLAB
        return GITLAB

    def gitlab(self, bot, update, user_data):
        text = update.message.text
        user_data["subscriptions"]["gitlab"] = text.split(", ")
        user_data.pop("STATE")
        send_post(user_data)
        update.message.reply_text("DONE!")
        return ConversationHandler.END

    def skip_github(self, bot, update, user_data):
        update.message.reply_text("Please send gitlab ids you want to subscribe to by seperating them with a comma and space")
        update.message.reply_text("Or you can /skip")
        user_data["subscriptions"] = {}
        user_data["subscriptions"]["github"] = []
        user_data["STATE"] = GITLAB
        return GITLAB

    def skip_gitlab(self, bot, update, user_data):
        user_data.pop("STATE")
        user_data["subscriptions"]["gitlab"] = []
        send_post(user_data)
        update.message.reply_text("DONE!")
        return ConversationHandler.END

    def cancel(self, bot, update, user_data):
        user_data.clear()
        update.message.reply_text("Subscription job is cancelled.")
        return ConversationHandler.END

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "{}" caused error "{}"'.format(update, error))

    def wrong_answer(self, bot, update, user_data):
        update.message.reply_text("This was an unexpected answer. Would you like to /cancel ?")
        return user_data["STATE"]

def run_job_queue(bot):
    try:
        redix = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        while True:
            # get job from redis
            _, job = redix.brpop(TELEGRAM_WORKER_QUEUE)
            job = json.loads(job)
            message = "Hello this is your periodic star reminder and these are the lucky repos:\n"
            for repo in job["repos"]:
                message = "{}\n--\t[{}]({})".format(message, repo["name"], repo["url"])
            message = "{}".format(message)
            try:
                bot.send_message(int(job['to']), message, parse_mode="Markdown", disable_web_page_preview=True)
            except error.BadRequest as e:
                logger.error("{}, UserID: {}".format(e, job["to"]))
            except error.Unauthorized as e:
                logger.error("{}, UserID: {}".format(e, job["to"]))
            # report job done.
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def send_post(user_data):
    r = requests.post(API_URL, data=json.dumps(user_data), headers={"content-type": "application/json"})

def main():
    bot = Bot(TOKEN)
    try:
        run_job_queue(bot.bot)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt. Stopping...")
        bot.updater.stop()
        return

if __name__ == '__main__':
    main()
