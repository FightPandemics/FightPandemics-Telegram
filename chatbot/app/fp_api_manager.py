import requests
import json
from chatbot.app import FP_BASE_URL


def login_fp(email, password):
    payload = {
        'email': email,
        'password': password
    }
    url = FP_BASE_URL + "auth/login"
    headers = {'content-type': 'application/json'}

    s = requests.Session()
    response = s.post(url, data=json.dumps(payload), headers=headers)
    response_json = response.json()
    if "emailVerified" in response_json and response_json['emailVerified']:
        return response_json['user']['id'], response_json['token'],

    return None, None


def create_fp_account(email, password):
    payload = {
        "email": email,
        "password": password,
        "confirmPassword": password
    }

    url = FP_BASE_URL + "auth/signup"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        p = s.post(url, data=json.dumps(payload), headers=headers)
        print(p.content)


def post_comment(token, user_id, post_id, content):
    payload = {
        "actorId": user_id,
        "content": content
    }
    url = FP_BASE_URL + "posts/{}/comments".format(post_id)
    headers = {'content-type': 'application/json'}

    s = requests.Session()
    s.headers['Authorization'] = 'Bearer {}'.format(token)
    req = s.post(url, data=json.dumps(payload), headers=headers)

    if req.status_code == 200:
        print(req.content)
        return req.json()
    else:
        return "Unable to connect to FightPandemics"


def get_posts(payload):
    url = FP_BASE_URL + "posts"
    headers = {'content-type': 'application/json'}
    s = requests.Session()
    response = s.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_post(post_id):
    url = FP_BASE_URL + "posts/" + post_id
    s = requests.Session()
    req = s.get(url)
    if req.status_code == 200:
        return req.json()
    else:
        return "Unable to connect to FightPandemics"


def get_current_user_profile(token):
    url = FP_BASE_URL + "users/current"
    s = requests.Session()
    s.headers['Authorization'] = 'Bearer {}'.format(token)
    req = s.get(url)

    if req.status_code == 200:
        return req.json()
    else:
        return "Unable to connect to FightPandemics"


def get_user_location(latitude, longitude):
    payload = {
        'lat': latitude,
        'lng': longitude
    }
    url = FP_BASE_URL + "geo/location-reverse-geocode"
    s = requests.Session()
    response = s.get(url, params=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to fetch location"
