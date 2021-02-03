import requests
import json
from chatbot.app.constants import FP_BASE_URL


def login_fp(email, password):
    payload = {
        'email': email,
        'password': password
    }
    url = FP_BASE_URL + "auth/login"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        response = s.post(url, data=json.dumps(payload), headers=headers)
    response_json = response.json()
    if not response_json.get('emailVerified'):
        return None, None

    return response_json['user']['id'], response_json['token'],


def create_fp_account(email, password):
    payload = {
        "email": email,
        "password": password,
        "confirmPassword": password
    }

    url = FP_BASE_URL + "auth/signup"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        response = s.post(url, data=json.dumps(payload), headers=headers)
    return response.json()


def post_comment(token, user_id, post_id, content):
    payload = {
        "actorId": user_id,
        "content": content
    }
    url = FP_BASE_URL + f"posts/{post_id}/comments"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        s.headers['Authorization'] = f'Bearer {token}'
        response = s.post(url, data=json.dumps(payload), headers=headers)

    _check_status_code(response)
    return response.json()


def get_posts(payload):
    url = FP_BASE_URL + "posts"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        response = s.get(url, params=payload, headers=headers)

    _check_status_code(response)
    return response.json()


def get_post(post_id):
    url = FP_BASE_URL + "posts/" + post_id

    with requests.Session() as s:
        response = s.get(url)

    _check_status_code(response)
    return response.json()


def get_current_user_profile(token):
    url = FP_BASE_URL + "users/current"

    with requests.Session() as s:
        s.headers['Authorization'] = 'Bearer {}'.format(token)
        response = s.get(url)

    _check_status_code(response)
    return response.json()


def get_user_location(latitude, longitude):
    payload = {
        'lat': latitude,
        'lng': longitude
    }
    url = FP_BASE_URL + "geo/location-reverse-geocode"

    with requests.Session() as s:
        response = s.get(url, params=payload)

    _check_status_code(response)
    return response.json()


def _check_status_code(response):
    if response.status_code != 200:
        raise ConnectionError("Unable to connect to FightPandemics")
