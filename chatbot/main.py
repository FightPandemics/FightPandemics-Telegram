import sys
import logging
from argparse import ArgumentParser

from telegram.ext import Updater  #, CommandHandler, CallbackQueryHandler

from chatbot.app import handlers, constants


# Enable logging
def setup_logging(log_level):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level.upper(),
    )


def main(log_level="INFO"):
    """Start the bot"""
    setup_logging(log_level=log_level)

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    if len(constants.TELEGRAM_TOKEN) == 0:
        raise ValueError("Please provide a valid telegram token")

    updater = Updater(constants.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(handlers.MainMenuCmdHandler)
    dp.add_handler(handlers.StartCmdHandler)
    dp.add_handler(handlers.HelpCmdHandler)
    # dp.add_handler(CommandHandler("start", handlers.start))
    # dp.add_handler(CommandHandler("help", handlers.help_command))
    # dp.add_handler(CommandHandler("mainmenu", handlers.main_menu))

    # Conversation handlers
    dp.add_handler(handlers.LoginConvHandler)
    dp.add_handler(handlers.CreatePostConvHandler)
    # for pattern in ["request_help", "offer_help"]:
    #     dp.add_handler(handlers.create_post_handler(pattern))

    # Callback query handlers
    dp.add_handler(handlers.AboutQueryHandler)
    dp.add_handler(handlers.SignoutQueryHandler)
    dp.add_handler(handlers.ViewMyProfileQueryHandler)
    dp.add_handler(handlers.ViewMyPostsQueryHandler)
    dp.add_handler(handlers.DisplaySelectedPostsQueryHandler)
    # dp.add_handler(CallbackQueryHandler(handlers.about, pattern='about'))
    # dp.add_handler(CallbackQueryHandler(handlers.signout, pattern='signout'))
    # dp.add_handler(CallbackQueryHandler(handlers.view_my_profile, pattern='view_my_profile'))
    # dp.add_handler(CallbackQueryHandler(handlers.view_my_posts, pattern='view_my_posts'))
    # dp.add_handler(CallbackQueryHandler(handlers.display_selected_post, pattern='display_selected_post'))

    # To start polling Telegram for any chat updates on Telegram
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # this command block the script until the user sends a command to break from the Python script
    updater.idle()


def parse_args():
    parser = ArgumentParser()
    log_levels = ["debug", "info", "warning", "error", "critical"]
    parser.add_argument(
        '--log-level',
        type=str,
        choices=log_levels,
        default="info",
        required=False,
        help="logging level",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(log_level=args.log_level)
