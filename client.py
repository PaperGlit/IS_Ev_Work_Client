import re
import requests
from requests import Session


class Client:
    @staticmethod
    def is_valid_username(user_name):
        return bool(re.match(r"^[a-zA-Z- ]{1,128}$", user_name))

    @staticmethod
    def is_valid_login(user_login):
        return bool(re.match("^[a-zA-Z0-9_]{3,30}$", user_login))

    @staticmethod
    def is_valid_password(password):
        return bool(re.match("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&-+=()])(?=\\S+$).{8,20}$", password))

    @staticmethod
    def rsa_encode(message, public_key):
        n, e = public_key
        encrypted_message = [pow(ord(char), e, n) for char in message]
        return encrypted_message

    @staticmethod
    def get_public_key(session):
        server_url = "https://127.0.0.1:5000/key"
        try:
            response = session.get(server_url, verify=False)
            public_key = response.json()["key"]
            if not public_key:
                raise Exception("Public key not found")
            return public_key
        except requests.exceptions.RequestException:
            raise Exception("Public key not found")

    @staticmethod
    def login(username, password):
        if not Client.is_valid_login(username):
            raise ValueError("Please enter a valid login")
        if not Client.is_valid_password(password):
            raise ValueError("Please enter a valid password")

        server_url = "https://127.0.0.1:5000/login"

        with Session() as session:
            public_key = Client.get_public_key(session)
            encoded_username = Client.rsa_encode(username, public_key)
            encoded_password = Client.rsa_encode(password, public_key)

            payload = {
                "login": encoded_username,
                "password": encoded_password
            }

            try:
                headers = {'Content-Type': 'application/json'}
                response = session.post(server_url, json=payload, headers=headers, verify=False)
                if response.status_code == 200:
                    return response.json()["status"]
                else:
                    raise ValueError("An error occurred: " + response.json()["status"])
            except requests.exceptions.RequestException as e:
                raise ValueError("An error occurred: " + str(e))

    @staticmethod
    def register(first_name, username, password):
        if not Client.is_valid_username(first_name):
            raise ValueError("Please enter a valid first name")
        if not Client.is_valid_login(username):
            raise ValueError("Please enter a valid login")
        if not Client.is_valid_password(password):
            raise ValueError("Please enter a valid password")

        server_url = "https://127.0.0.1:5000/register"

        with Session() as session:
            public_key = Client.get_public_key(session)
            encoded_first_name = Client.rsa_encode(first_name, public_key)
            encoded_username = Client.rsa_encode(username, public_key)
            encoded_password = Client.rsa_encode(password, public_key)

            payload = {
                "name": encoded_first_name,
                "login": encoded_username,
                "password": encoded_password
            }

            try:
                headers = {'Content-Type': 'application/json'}
                response = session.post(server_url, json=payload, headers=headers, verify=False)
                if response.status_code == 201:
                    return response.json()["status"]
                else:
                    raise ValueError("An error occurred: " + response.json()["status"])
            except requests.exceptions.RequestException as e:
                raise ValueError("An error occurred: " + str(e))