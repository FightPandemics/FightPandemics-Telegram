def _reply_to_callback_query(update, context, text=None, keyboard=None):
    """Reply to an callback query, i.e. user clicks a button."""
    callback_query = update.callback_query
    assert callback_query is not None, "No callback query in update"
    callback_query.answer()
    context.bot.send_message(
        chat_id=callback_query.message.chat_id,
        text=text,
        reply_markup=keyboard,
    )


def _reply_to_message(update, context, text=None, keyboard=None):
    message = update.message
    assert message is not None, "No message in update"
    message.reply_text(
        text=text,
        reply_markup=keyboard,
    )


def reply(update, context, text=None, keyboard=None):
    callback_query = update.callback_query
    message = update.message
    if callback_query is not None:
        _reply_to_callback_query(
            update=update,
            context=context,
            text=text,
            keyboard=keyboard,
        )
        return
    if message is not None:
        _reply_to_message(
            update=update,
            context=context,
            text=text,
            keyboard=keyboard,
        )
        return
    raise RuntimeError("Couldn't reply, neither message or callback query")
