import uuid
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


class GigaChatClient:
    AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    def __init__(self):
        self.client_id = settings.GIGACHAT_CLIENT_ID
        self.secret = settings.GIGACHAT_SECRET

    def get_access_token(self) -> str:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
        }

        payload = {"scope": "GIGACHAT_API_PERS"}

        res = requests.post(
            url=self.AUTH_URL,
            headers=headers,
            auth=HTTPBasicAuth(self.client_id, self.secret),
            data=payload,
            verify=False,
        )
        res.raise_for_status()
        return res.json()["access_token"]

    def ask(self, prompt: str) -> str:
        token = self.get_access_token()

        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": prompt}],
        }

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        res = requests.post(
            self.CHAT_URL,
            json=payload,
            headers=headers,
            verify=False,
        )
        res.raise_for_status()

        return res.json()["choices"][0]["message"]["content"]
