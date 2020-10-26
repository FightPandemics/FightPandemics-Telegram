import requests
import json
from app.constants import FP_BASE_URL


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


def get_posts(filter_params_dict, objective):
    url = FP_BASE_URL + "posts"

    # To emulate JSON.stringify behavior
    # https://github.com/FightPandemics/FightPandemics/blob/8a749609d580c9c23c5ec7fa64f44daa568f9467/client/src/pages/Feed.js#L445
    encoded_filters = json.dumps(filter_params_dict, separators=(',', ':'))
    print(encoded_filters)

    payload = {
        "filter": encoded_filters,
        "objective": objective
    }
    headers = {'content-type': 'application/json'}
    s = requests.Session()
    #s.headers['Authorization'] = 'Bearer {}'.format(token)
    response = s.get(url, params=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return "Unable to connect to FightPandemics"


def get_user_posts(user_id):
    url = FP_BASE_URL + "posts"

    s = requests.Session()
    req = s.get(url)

    if req.status_code == 200:
        return req.json()
    else:
        return "Unable to connect to FightPandemics"


def get_current_user_profile(token):
    url = FP_BASE_URL + "/users/current"
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


if __name__ == "__main__":
    # get_user_posts('5f3d54538689251600c5d399')
    #print(get_user_location(42.349367, -71.083636))
    print(get_posts({"type": ["Medical Supplies"]}))
