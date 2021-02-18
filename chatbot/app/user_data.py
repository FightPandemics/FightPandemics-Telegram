from chatbot.app import patterns

# User data keys
USER_ID = 'user_id'
USERNAME = 'username'
TOKEN = 'token'
LOCATION = 'location'

POST_TITLE = "post_title"
POST_DESCRIPTION = "post_description"
POST_CATEGORIES = "categories"
POST_VISIBILITY = "post_visibility"
POST_DURATION = "post_duration"
POST_OBJECTIVE = "post_objective"

VIEW_PAGE_ID = 'page_id'
VIEW_POST_ID = 'post_id'
VIEW_POST_IDS = 'post_ids'
VIEW_POST_PAYLOAD = 'post_payload'

OBJECTIVE_REQUEST = "request"
OBJECTIVE_OFFER = "offer"

USER_INFO = [
    USER_ID,
    USERNAME,
    TOKEN,
    LOCATION,
]

POST_INFO = [
    POST_TITLE,
    POST_DESCRIPTION,
    POST_CATEGORIES,
    POST_VISIBILITY,
    POST_DURATION,
    POST_OBJECTIVE,
]

VIEW_INFO = [
    VIEW_PAGE_ID,
    VIEW_POST_ID,
    VIEW_POST_IDS,
    VIEW_POST_PAYLOAD,
]

ALL_INFO = USER_INFO + POST_INFO + VIEW_INFO


def is_user_signed_in(context):
    return context.user_data.get(USER_ID) is not None


def objective_from_pattern(pattern):
    if pattern in [patterns.REQUEST_HELP, patterns.REQUEST_HELP_POSTS]:
        return OBJECTIVE_REQUEST
    elif pattern in [patterns.OFFER_HELP, patterns.OFFER_HELP_POSTS]:
        return OBJECTIVE_OFFER
    else:
        raise ValueError(f"Unexpected pattern {pattern}")
