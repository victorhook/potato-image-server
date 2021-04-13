from django.conf import settings
import requests

class Proxy:

    @staticmethod
    def _request(endpoint: str) -> str:
        r = requests.get(f'{settings.PROXY_HOST}/{endpoint}',
                        headers={
                            'Authorization': f'Basic {settings.PROXY_AUTH}'
                            })
        print(r)

    @staticmethod
    def get_dates() -> list:
        html = Proxy._request('')
        return []

    @staticmethod
    def get_images(date: str) -> list:
        html = Proxy._request(date)
        return []


if __name__ == '__main__':


    print(r.text)