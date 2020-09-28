import requests
import json
from app.constants import FP_BASE_URL


def login_fp(email, password):
    payload = {
        'email': email,
        'password': password
    }
    url = FP_BASE_URL+"auth/login"
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

    url = FP_BASE_URL+"auth/signup"
    headers = {'content-type': 'application/json'}

    with requests.Session() as s:
        p = s.post(url, data=json.dumps(payload), headers=headers)
        print(p.content)


def get_fp_post(token):
    url = FP_BASE_URL+"posts"

    s = requests.Session()
    s.headers['Authorization'] = 'Bearer {}'.format(token)
    req = s.get(url)

    if req.status_code == 200:
        return req.json()
    else:
        return "Unable to connect to FightPandemics"


def get_user_posts():
    url = FP_BASE_URL+"posts"

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


if __name__ == "__main__":
    get_user_posts('5f3d54538689251600c5d399')


