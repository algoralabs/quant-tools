import json

import requests


class ApiGateway(object):
    def __init__(self,
                 username,
                 password,
                 base_host="api.algoralabs.com"
                 ):
        self.http_url = f"https://{base_host}"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.username = username
        self.password = password
        self.BEARER_TOKEN = None
        self.REFRESH_TOKEN = None
        self.authenticate(username=username, password=password)
        self.retry = True

    def authenticate(self, username, password):
        data = json.dumps({"username": username, "password": password})

        response = requests.post(self.http_url + "/login", data=data, headers=self.headers)

        if response.status_code == 200:
            self.BEARER_TOKEN = response.json()['access_token']
            self.REFRESH_TOKEN = response.json()['refresh_token']
        else:
            response.raise_for_status()

    def refresh_token(self):
        data = json.dumps({'refresh_token': self.REFRESH_TOKEN})

        response = requests.post(self.http_url + '/refresh_token', data=data, headers=self.headers)

        if response.status_code == 200:
            self.BEARER_TOKEN = response.json()['access_token']
            self.REFRESH_TOKEN = response.json()['refresh_token']
        else:
            self.authenticate(username=self.username, password=self.password)

    def authenticated_request(self, uri, method='GET', **kwargs):
        response = requests.request(method=method, url=f'{self.http_url}{uri}',
                                    headers={'Authorization': f'Bearer {self.BEARER_TOKEN}'},
                                    **kwargs)

        if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
            self.retry = True
            try:
                return response.json()
            except Exception as e:
                print(e)
                return None
        elif self.retry and response.status_code == 401:
            # refresh token and retry
            self.retry = False
            self.refresh_token()
            self.authenticated_request(uri, method, **kwargs)
        else:
            response.raise_for_status()
