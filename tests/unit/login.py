from chatbot.app import user_data


def login_user(mock_bot, user_id=0, user_name="user_name"):
    user_info = {
        user_data.USERNAME: user_name,
        user_data.USER_ID: user_id,
    }
    for key, value in user_info.items():
        mock_bot.set_user_data_entry(key, value)
