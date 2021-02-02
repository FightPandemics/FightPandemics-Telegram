from chatbot.app import fp_api_manager as fpapi

# TODO not used anywhere yet, should be updated


def get_user_comment(update, context):
    if "token" in context.user_data:
        reply_text = "Please type your comment below"
        update.effective_message.reply_text(reply_text)
    else:
        update.effective_message.reply_text(text="To post a comment you need to login first")


def post_comment(update, context):
    token = context.user_data["token"]
    user_id = context.user_data["user_id"]
    post_id = context.user_data["post_id"]
    content = update.message.text
    fpapi.post_comment(token, user_id, post_id, content)
    update.effective_message.reply_text(text='Comment posted')
