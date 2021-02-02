def reply_to_callback_query(update, context, text=None, keyboard=None):
    """Reply to an callback query, i.e. user clicks a button."""
    callback_query = update.callback_query
    callback_query.answer()
    context.bot.send_message(
        chat_id=callback_query.message.chat_id,
        text=text,
        reply_markup=keyboard,
    )
