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

    with requests.Session() as s:
        p = s.post(url, data=json.dumps(payload), headers=headers)
        print(p.content)


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


def get_fp_post():
    url = FP_BASE_URL+"posts"

    with requests.Session() as s:
        p = s.get(url)
        if p.status_code == 200:
            return p.json()
        else:
            return "Unable to connect to FightPandemics"


def get_current_user_profile():
    # make it dynamic once authentication works. For testing purpose I have hardcoded this value.
    url = FP_BASE_URL+"users/5f3d54538689251600c5d399"

    with requests.Session() as s:
        p = s.get(url)
        if p.status_code == 200:
            return p.json()
        else:
            return "Unable to connect to FightPandemics"

