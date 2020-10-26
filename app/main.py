import logging
from app.handlers import *
from app.constants import TELEGRAM_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    if len(TELEGRAM_TOKEN) == 0:
        raise ValueError("Please provide a valid telegram token")

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    ############ add all handlers here #########################################################

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("mainmenu", main_menu))
    # dp.add_handler(CommandHandler("viewposts",view_posts))
    dp.add_handler(login_handler())
    dp.add_handler(offer_help_conv_handler())

    ########################  update dispatcher  #########################################################

    # we’ll use the dispatcher to add commands.
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='menu'))
    dp.add_handler(CallbackQueryHandler(about, pattern='about'))
    dp.add_handler(CallbackQueryHandler(request_help, pattern='request_help'))
    dp.add_handler(CallbackQueryHandler(login, pattern='login'))
    #dp.add_handler(CallbackQueryHandler(view_posts, pattern='view_posts'))
    dp.add_handler(CallbackQueryHandler(view_profile, pattern='view_profile'))
    dp.add_handler(CallbackQueryHandler(create_posts, pattern='create_posts'))

    # To start polling Telegram for any chat updates on Telegram
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # this command block the script until the user sends a command to break from the Python script
    updater.idle()


if __name__ == '__main__':
    main()
