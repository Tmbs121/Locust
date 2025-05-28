import random
import re

import pytest
from playwright.sync_api import expect

from api_ui_common_modules import parse_user_credentials_from_csv
from api_ui_common_modules.parse_user_credentials_from_csv import LoginWithCreds


@pytest.fixture()
def set_up_tear_down(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto("http://172.23.176.159/opencart/upload")
    expect(page).to_have_title(re.compile("Your Store"))
    yield page


@pytest.fixture()
def credentials_pair(self=LoginWithCreds):
    user_credentials = parse_user_credentials_from_csv.LoginWithCreds.read_creds_from_csv(self)
    credentials_pair = random.choice(list(user_credentials.items()))
    return credentials_pair


@pytest.fixture()
def username(credentials_pair):
    user_n = credentials_pair[0]
    yield user_n


@pytest.fixture()
def password(credentials_pair):
    psw = credentials_pair[1]
    yield psw
