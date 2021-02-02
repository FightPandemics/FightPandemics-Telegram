import json

from telegram.ext import ConversationHandler, CallbackQueryHandler

from chatbot.app import views, keyboards
from chatbot.app import fp_api_manager as fpapi
from chatbot.app.user_data import (
    CATEGORIES_KEY,
)


def view_my_profile(update, context):
    """ Display user profile"""

    if "token" in context.user_data:
        token = context.user_data["token"]
        user_profile_json = fpapi.get_current_user_profile(token=token)
        user_info_view = views.UserProfile(user_profile_json).display()
        update.effective_message.reply_text(text=user_info_view)
    else:
        update.effective_message.reply_text("Please login to view your profile")


def view_posts(update, context):
    """ Display the relevant posts to the user based on location, type of help.
    Display title of post, actual post(limited information), and comments on posts of user"""
    list_to_display = []
    post_id_list = []
    filter_params_dict = {CATEGORIES_KEY: list(context.user_data[CATEGORIES_KEY])}
    # To emulate JSON.stringify behavior
    encoded_filters = json.dumps(filter_params_dict, separators=(',', ':'))

    post_payload = {
        "filter": encoded_filters,
        "objective": context.user_data['objective'],
        "limit": 10,
        "skip": 0
    }
    # keep a copy of post_payload in user_data for future calls
    context.user_data['post_payload'] = post_payload
    posts_json = fpapi.get_posts(post_payload)
    context.user_data['page'] = 0
    post_categories = ", ".join(context.user_data[CATEGORIES_KEY])
    for idx, post in enumerate(posts_json):
        post_id_list.append(post['_id'])
        post_highlight = views.UserPost(post).display()
        list_to_display.append(str(idx + 1) + ".  " + post_highlight)
    context.user_data['post_ids'] = post_id_list
    if list_to_display:
        page = context.user_data['page'] + 1
        objective = context.user_data['objective']
        reply_text = (
            f"Page {page} . Viewing {objective} posts for {post_categories} help category.\n\n"
            "\n".join(list_to_display)
        )
        update.effective_message.reply_text(
            text=reply_text,
            reply_markup=keyboards.view_posts(),
        )

    else:
        reply_text = (
            f"No post found for {post_categories} category.\n"
            "Please create a new post."
        )
        update.effective_message.reply_text(
            text=reply_text,
            reply_markup=keyboards.create_post(),
        )

    context.user_data[CATEGORIES_KEY] = set()
    return ConversationHandler.END


def view_my_posts(update, context):
    """ Display the title of post, actual post(limited information), and comments on posts of user"""

    list_to_display = []
    post_id_list = []
    user_id = context.user_data['user_id']
    post_payload = {
        "authorId": user_id,
        "limit": 10,
        "skip": 0
    }
    context.user_data['post_payload'] = post_payload posts_json = fpapi.get_posts(post_payload)
    if posts_json is not None:
        context.user_data['page'] = 0
    for idx, post in enumerate(posts_json):
        post_id_list.append(post['_id'])
        post_highlight = views.UserPost(post).display()
        list_to_display.append(str(idx + 1) + ".  " + post_highlight)
    context.user_data['post_ids'] = post_id_list
    if list_to_display:
        header_message = "Page {} of your posts \n".format(context.user_data['page'] + 1)
        reply_text = "{} \n {}".format(header_message, "\n".join(list_to_display))
        update.effective_message.reply_text(
            text=reply_text,
            reply_markup=keyboards.view_posts(),
        )


def display_selected_post(update, context):
    choice = update.callback_query.data.split('_')[-1]
    if choice in [str(n) for n in range(1, 11)]:
        post_id = context.user_data['post_ids'][int(choice) - 1]
        post_json = fpapi.get_post(post_id)
        reply_text = views.Post(post_json=post_json).display()
        context.user_data["post_id"] = post_id
        update.effective_message.reply_text(
            text=reply_text,
            reply_markup=keyboards.display_selected_post(),
        )
    elif choice == 'next' or choice == 'prev':
        context.user_data['post_ids'] = []
        list_to_display = []
        post_id_list = []
        updated_page_id = context.user_data['page']
        if choice == 'next':
            updated_page_id += 1
        else:
            updated_page_id -= 1

        posts_to_skip = 10 * updated_page_id
        context.user_data['post_payload']['skip'] = posts_to_skip
        posts_json = fpapi.get_posts(context.user_data['post_payload'])
        if posts_json is not None:
            context.user_data['page'] = updated_page_id

        for idx, post in enumerate(posts_json):
            post_id_list.append(post['_id'])
            post_highlight = views.UserPost(post).display()
            list_to_display.append(str(idx + 1) + ".  " + post_highlight)
        context.user_data['post_ids'] = post_id_list
        if CATEGORIES_KEY in context.user_data:
            post_categories = ", ".join(context.user_data[CATEGORIES_KEY])
            header_message = "Page {} . Viewing {} posts for {} help category.\n\n".format(
                context.user_data['page']+1, context.user_data['objective'], post_categories)
        else:
            header_message = "Page {} of your posts \n".format(context.user_data['page']+1)
        if list_to_display:
            reply_text = "{} \n {}".format(header_message, "\n".join(list_to_display))
            update.effective_message.reply_text(
                text=reply_text,
                reply_markup=keyboards.view_posts(),
            )


ViewMyProfileQueryHandler = CallbackQueryHandler(view_my_profile, pattern='view_my_profile')
ViewMyPostsQueryHandler = CallbackQueryHandler(view_my_posts, pattern='view_my_posts')
DisplaySelectedPostsQueryHandler = CallbackQueryHandler(display_selected_post, pattern='display_selected_post')
ViewPostsQueryHandler = CallbackQueryHandler(view_posts, pattern='view_posts')
