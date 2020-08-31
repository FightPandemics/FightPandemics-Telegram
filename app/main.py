import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler)
from app.handlers import *
from app.constants import TELEGRAM_TOKEN

# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define command handlers which usually take the two arguments update and context and requires both.
# Error handlers also receive the raised TelegramError object in error.
# update.message.reply_text automatically adds the reply only to the specific chat.

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Do you want to request help or offer help? Type /mainmenu command for more details.')


# noncommand i.e message - echo/repeat the message on Telegram
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


# we use the reply_text method, replying with update.message.text sends the message chat text back to the user.
# For example hi, bye etc.


################################ main #############################################
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # command handler will execute when the user enters a command.
    # For example, /start and will execute the callback function start.
    # This command automatically executes when user type commands or press buttons

    ############ adding handlers #########################################################

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("request", request_help)) (can be deleted)
    dp.add_handler(CommandHandler("mainmenu", main_menu))

    # dp.add_handler(CommandHandler("login", login_fp))
    # filter here so that this message handler Filters everything except text
    # in case user post something other than text in their messages (such as images or video)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


    ########################  update dispatcher  #########################################################

    # we’ll use the dispatcher to add commands.

    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='menu'))
    updater.dispatcher.add_handler(CallbackQueryHandler(about, pattern='about'))
    updater.dispatcher.add_handler(CallbackQueryHandler(offer_help, pattern='offer_help'))
    updater.dispatcher.add_handler(CallbackQueryHandler(request_help, pattern='request_help'))
    updater.dispatcher.add_handler(CallbackQueryHandler(login_fp, pattern='login_fp'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(signup_fp, pattern='signup'))
    updater.dispatcher.add_handler(CallbackQueryHandler(view_posts, pattern='view_posts'))
    updater.dispatcher.add_handler(CallbackQueryHandler(view_profile, pattern='view_profile'))



    # To start polling Telegram for any chat updates on Telegram
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # this command block the script until the user sends a command to break from the Python script
    updater.idle()


if __name__ == '__main__':
    main()
