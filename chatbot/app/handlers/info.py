from telegram.ext import CommandHandler, CallbackQueryHandler

from chatbot.app import patterns


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Do you want to request help or offer help? '
        'Type /mainmenu command for more details.'
    )


def about(update, context):
    """Send a message to FP url when the command /about is issued."""

    fp_about_message = "Please visit https://fightpandemics.com/about-us"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=fp_about_message,
    )


HelpCmdHandler = CommandHandler('help', help)
AboutQueryHandler = CallbackQueryHandler(about, pattern=patterns.ABOUT_FIGHTPANDEMICS)
