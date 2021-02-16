def reply_to_callback_query(update, context, text=None, keyboard=None):
    """Reply to an callback query, i.e. user clicks a button."""
    callback_query = update.callback_query
    assert callback_query is not None, "No callback query in update"
    callback_query.answer()
    context.bot.send_message(
        chat_id=callback_query.message.chat_id,
        text=text,
        reply_markup=keyboard,
    )


def reply_to_message(update, context, text=None, keyboard=None):
    message = update.message
    assert message is not None, "No message in update"
    message.reply_text(
        text=text,
        reply_markup=keyboard,
    )
