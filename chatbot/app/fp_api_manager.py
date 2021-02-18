import requests
import json
from enum import Enum, auto
from chatbot.app.constants import FP_BASE_URL

VALID_STATUS_CODES = [200]


class Error(Enum):
    INVALID_LOGIN = auto()
    NO_CONNECTION = auto()
    INVALID_STATUS_CODE = auto()


def login_fp(email, password):
    payload = {
        'email': email,
        'password': password
    }
    url = FP_BASE_URL + "auth/login"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        response = _try_post(s, url, data=json.dumps(payload), headers=headers)
    if isinstance(response, Error):
        return response
    if not response.get('emailVerified'):
        return Error.INVALID_LOGIN
    return response


def create_fp_account(email, password):
    payload = {
        "email": email,
        "password": password,
        "confirmPassword": password
    }

    url = FP_BASE_URL + "auth/signup"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        return _try_post(s, url, data=json.dumps(payload), headers=headers)


def post_comment(token, user_id, post_id, content):
    payload = {
        "actorId": user_id,
        "content": content
    }
    url = FP_BASE_URL + f"posts/{post_id}/comments"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        s.headers['Authorization'] = f'Bearer {token}'
        return _try_post(s, url, data=json.dumps(payload), headers=headers)


def get_posts(payload):
    url = FP_BASE_URL + "posts"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        return _try_get(s, url, params=payload, headers=headers)


def get_post(post_id):
    url = FP_BASE_URL + "posts/" + post_id

    with requests.Session() as s:
        return _try_get(s, url)


def get_current_user_profile(token):
    url = FP_BASE_URL + "users/current"

    with requests.Session() as s:
        s.headers['Authorization'] = 'Bearer {}'.format(token)
        return _try_get(s, url)


def get_user_location(latitude, longitude):
    payload = {
        'lat': latitude,
        'lng': longitude
    }
    url = FP_BASE_URL + "geo/location-reverse-geocode"

    with requests.Session() as s:
        return _try_get(s, url, params=payload)


class StatusCodeError(ConnectionError):
    pass


def _check_status_code(response):
    if response.status_code not in VALID_STATUS_CODES:
        raise StatusCodeError(f"Unable to connect to FightPandemics ({response})")


def _try_post(session, *args, **kwargs):
    return _try_request(session, "post", *args, **kwargs)


def _try_get(session, *args, **kwargs):
    return _try_request(session, "get", *args, **kwargs)


def _try_request(session, method, *args, **kwargs):
    try:
        response = getattr(session, method)(*args, **kwargs)
        _check_status_code(response)
        return response.json()
    except requests.exceptions.ConnectionError:
        return Error.NO_CONNECTION
    except StatusCodeError:
        return Error.INVALID_STATUS_CODE
