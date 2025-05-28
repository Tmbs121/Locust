from locust import User, constant, os
import csv

user_credentials = {}


class LoginWithCreds(User):

    def read_creds_from_csv(self) -> dict[str, str]:
        global user_credentials
        with open(os.path.join("test_data", "opencart_creds.csv"), 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip the headers in the opencart_creds.csv
            user_credentials = dict(reader)
            return user_credentials

    def use_each_cred_pair_only_once(self) -> None:
        for username in user_credentials:
            if len(user_credentials) > 0:
                user_credentials.pop(username)

    tasks = [read_creds_from_csv, use_each_cred_pair_only_once]
    wait_time = constant(1)
