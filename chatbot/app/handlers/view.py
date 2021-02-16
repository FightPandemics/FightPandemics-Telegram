import json

from telegram.ext import ConversationHandler, CallbackQueryHandler

from chatbot.app import views, keyboards, patterns, handlers
from chatbot.app import fp_api_manager as fpapi
from chatbot.app.user_data import (
    CATEGORIES_KEY,
)


USER_CHOICE_NEXT = 'next'
USER_CHOICE_PREV = 'prev'
POSTS_PER_PAGE = 10


def view_my_profile(update, context):
    """ Display user profile"""
    token = context.user_data.get("token")
    if token is None:
        update.effective_message.reply_text("Please login to view your profile")
        return

    response = fpapi.get_current_user_profile(token=token)
    if isinstance(response, fpapi.Error):  # TODO handle error better
        raise ConnectionError("Could not get user profile")
    user_info_view = views.UserProfile(response).display()
    update.effective_message.reply_text(text=user_info_view)


def view_posts(update, context):
    """ Display the relevant posts to the user based on location, type of help.
    Display title of post, actual post(limited information), and comments on posts of user"""
    # TODO Why is the page set to 0 here?
    _set_user_page(context, page=0)
    payload = _get_posts_payload(context)
    posts = _get_posts(context, payload)
    _update_user_post_ids(context, posts)
    if len(posts) > 0:
        _handle_view_posts(
            update=update,
            context=context,
            posts=posts,
        )
    else:
        _handle_no_view_posts(
            update=update,
            context=context,
        )

    context.user_data[CATEGORIES_KEY] = set()
    return ConversationHandler.END


def view_my_posts(update, context):
    """Display the title of post, actual post(limited information), and comments on posts of user"""
    # TODO Why is the page set to 0 here?
    _set_user_page(context, page=0)
    payload = _get_my_posts_payload(context)
    posts = _get_posts(context, payload)
    _update_user_post_ids(context, posts)
    if len(posts):
        _handle_view_my_posts(
            update,
            context,
            posts,
        )
    # TODO what to do otherwise?


def display_selected_post(update, context):
    user_choice = update.callback_query.data.split('_')[-1]
    if _is_user_choice_post_id(user_choice):
        _handle_post_id_choice(
            update=update,
            context=context,
            user_choice=user_choice,
        )
    elif _is_user_choice_page_change(user_choice):
        _handle_page_change_choice(
            update=update,
            context=context,
            user_choice=user_choice,
        )
    else:
        raise ValueError(f"Unknown user choice: {user_choice}")


def _get_posts(context, payload):
    # keep a copy of post_payload in user_data for future calls - TODO is it used?
    context.user_data['post_payload'] = payload
    posts = fpapi.get_posts(payload)
    if isinstance(posts, fpapi.Error):  # TODO handle error better
        raise ConnectionError("Could not get posts")
    return posts


def _get_posts_payload(context):
    categories = context.user_data[CATEGORIES_KEY]
    filter_params_dict = {CATEGORIES_KEY: list(categories)}
    # To emulate JSON.stringify behavior
    encoded_filters = json.dumps(filter_params_dict, separators=(',', ':'))
    payload = {
        "filter": encoded_filters,
        "objective": context.user_data['objective'],
        "limit": 10,
        "skip": 0
    }
    return payload


def _update_user_post_ids(context, posts):
    post_ids = [post['_id'] for post in posts]
    context.user_data['post_ids'] = post_ids


def _handle_view_posts(update, context, posts):
    header_message = _get_header_message_with_categories(context)
    _show_posts_to_user(
        update=update,
        context=context,
        posts=posts,
        header_message=header_message,
    )


def _handle_no_view_posts(update, context):
    categories = _get_user_categories(context)
    formatted_categories = ", ".join(categories)
    reply_text = (
        f"No post found for {formatted_categories} category.\n"
        "Please create a new post."
    )
    update.effective_message.reply_text(
        text=reply_text,
        reply_markup=keyboards.create_post(),
    )


def _get_user_categories(context):
    return context.user_data[CATEGORIES_KEY]


def _format_posts(posts: list) -> str:
    formatted_posts = ""
    for idx, post in enumerate(posts):
        post_highlight = views.UserPost(post).display()
        real_idx = idx + 1
        formatted_posts += f"{real_idx}.  {post_highlight}\n"
    return formatted_posts


def _set_user_page(context, page):
    context.user_data['page'] = page


def _get_current_user_page(context):
    # TODO why is this plus one? Will currently always be 1?
    return context.user_data['page'] + 1


def _get_my_posts_payload(context):
    user_id = context.user_data['user_id']
    payload = {
        "authorId": user_id,
        "limit": 10,
        "skip": 0
    }
    return payload


def _handle_view_my_posts(update, context, posts):
    header_message = _get_header_message_user_posts(context)
    _show_posts_to_user(
        update=update,
        context=context,
        posts=posts,
        header_message=header_message,
    )


def _show_posts_to_user(update, context, posts, header_message):
    formatted_posts = _format_posts(posts)
    reply_text = f"{header_message}\n\n{formatted_posts}"
    handlers.util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply_text,
        keyboard=keyboards.view_posts(),
    )


def _is_user_choice_post_id(user_choice):
    return user_choice in [str(n) for n in range(1, 11)]


def _is_user_choice_page_change(user_choice):
    return user_choice in [USER_CHOICE_NEXT, USER_CHOICE_PREV]


def _get_updated_page_id(context, user_choice):
    updated_page_id = context.user_data['page']
    if user_choice == USER_CHOICE_NEXT:
        updated_page_id += 1
    elif user_choice == USER_CHOICE_PREV:
        updated_page_id -= 1
    else:
        raise ValueError(f"Unknown user choice: {user_choice}")
    return updated_page_id


def _get_posts_to_skip(updated_page_id):
    return POSTS_PER_PAGE * updated_page_id


def _handle_post_id_choice(update, context, user_choice):
    post_id = _get_real_post_id(context, user_choice)
    _update_user_post_id(context, post_id=post_id)
    _show_user_single_post(
        update=update,
        post_id=post_id,
    )


def _handle_page_change_choice(update, context, user_choice):
    updated_page_id = _get_updated_page_id(context, user_choice)
    payload = context.user_data['post_payload']
    payload['skip'] = _get_posts_to_skip(updated_page_id)
    posts = _get_posts(context, payload)
    _set_user_page(context, page=updated_page_id)
    _update_user_post_ids(context, posts)

    if CATEGORIES_KEY in context.user_data:
        header_message = _get_header_message_with_categories(context)
    else:
        header_message = _get_header_message_user_posts(context)

    if len(posts) > 0:
        _show_posts_to_user(
            update=update,
            context=context,
            posts=posts,
            header_message=header_message,
        )


def _update_user_post_id(context, post_id):
    context.user_data["post_id"] = post_id


def _get_real_post_id(context, user_choice):
    return context.user_data['post_ids'][int(user_choice) - 1]


def _show_user_single_post(update, post_id):
    post = fpapi.get_post(post_id)
    if isinstance(post, fpapi.Error):  # TODO handle error better
        raise ConnectionError("Could not get post")
    reply_text = views.Post(post_json=post).display()
    update.effective_message.reply_text(
        text=reply_text,
        reply_markup=keyboards.display_selected_post(),
    )


def _get_header_message_with_categories(context):
    formatted_categories = ", ".join(context.user_data[CATEGORIES_KEY])
    page = _get_current_user_page(context)
    objective = context.user_date['objective']
    return f"Page {page} . Viewing {objective} posts for {formatted_categories} help category."


def _get_header_message_user_posts(context):
    page = _get_current_user_page(context)
    return f"Page {page} of your posts"


ViewMyProfileQueryHandler = CallbackQueryHandler(view_my_profile, pattern=patterns.VIEW_MY_PROFILE)
ViewMyPostsQueryHandler = CallbackQueryHandler(view_my_posts, pattern=patterns.VIEW_MY_POSTS)
DisplaySelectedPostsQueryHandler = CallbackQueryHandler(display_selected_post, pattern=patterns.DISPLAY_SELECTED_POST)
ViewPostsQueryHandler = CallbackQueryHandler(view_posts, pattern=patterns.VIEW_POSTS)
