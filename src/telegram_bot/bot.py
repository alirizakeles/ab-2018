#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


api_url = "URL/v1/subscriptions"

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import requests
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMAIL, PERIOD, GITHUB, GITLAB, DONE = range(5)



class Bot:
    def __init__(self, token):
        updater = Updater(token)
        self.bot = updater.bot
        dp = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('subscribe', self.subscribe)],

            states={
                EMAIL: [MessageHandler(Filters.text,
                                               self.email,
                                               pass_user_data=True),
                                ],

                PERIOD: [MessageHandler(Filters.text,
                                               self.period,
                                               pass_user_data=True),
                                ],

                GITHUB: [MessageHandler(Filters.text,
                                              self.github,
                                              pass_user_data=True),
                               ],

                GITLAB: [MessageHandler(Filters.text,
                                              self.gitlab,
                                              pass_user_data=True),
                               ],

                DONE: [MessageHandler(Filters.text,
                                              self.done,
                                              pass_user_data=True),
                               ],
            },

            fallbacks=[MessageHandler(Filters.text,
                                          self.github,
                                          pass_user_data=True),
                           ]
        )

        dp.add_handler(conv_handler)
        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def subscribe(self, bot, update):
        update.message.reply_text("Please send your email address:")
        return EMAIL

    def email(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send your message period preference (weekly, daily, monthly):")
        user_data["email"] = text
        return PERIOD

    def period(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send github ids you want to subscribe to:")
        user_data["period"] = text
        return GITHUB

    def github(self, bot, update, user_data):
        text = update.message.text
        update.message.reply_text("Please send gitlab ids you want to subscribe to:")

        user_data["github"] = text.split(", ")
        return GITLAB

    def gitlab(self, bot, update, user_data):
        text = update.message.text
        user_data["gitlab"] = text.split(", ")
        user = update.message.from_user
        user_id = user.id
        user_data["telegramID"] = user_id
        print(user_data)
        return ConversationHandler.END

    def done(self, bot, update, user_data):
        user = update.message.from_user
        user_id = user.id
        print(user_data)
        return ConversationHandler.END

    def send_post(user_data):
        requests.post(api_url, data=json.dumps(user_data), headers={"content-type": "application/json"})

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    bot = Bot("539265705:AAFQLYfGn7mIkztFRgc3Ebb6xUXCDiBDWps")

if __name__ == '__main__':
    main()
