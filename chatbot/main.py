import logging
from argparse import ArgumentParser

from telegram.ext import Updater

from chatbot.app import handlers, constants


# Enable logging
def setup_logging(log_level):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level.upper(),
    )


def check_telegram_token():
    if len(constants.TELEGRAM_TOKEN) == 0:
        raise ValueError("Please provide a valid telegram token")


def main(log_level="INFO"):
    """Start the bot"""
    setup_logging(log_level=log_level)

    check_telegram_token()
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater(constants.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(handlers.MainMenuCmdHandler)
    dp.add_handler(handlers.HelpCmdHandler)

    # Conversation handlers
    dp.add_handler(handlers.LoginConvHandler)
    dp.add_handler(handlers.CreatePostConvHandler)
    dp.add_handler(handlers.ViewPostsConvHandler)

    # Callback query handlers
    dp.add_handler(handlers.AboutQueryHandler)
    dp.add_handler(handlers.SignoutQueryHandler)
    dp.add_handler(handlers.ViewMyProfileQueryHandler)
    dp.add_handler(handlers.ViewMyPostsQueryHandler)
    dp.add_handler(handlers.DisplaySelectedPostsQueryHandler)

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
