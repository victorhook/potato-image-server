from django.conf import settings

from .cache import cache

import base64
import requests
import re


RE_A_TAG: re.Pattern = re.compile('href="(.*)">(.*)<\/a>')


class Proxy:

    @staticmethod
    def _request(endpoint: str, as_bytes: bool = False) -> str:
        print('Sending to...', f'{settings.PROXY_HOST}/{endpoint}')
        r = requests.get(f'{settings.PROXY_HOST}/{endpoint}',
                        headers={
                            'Authorization': f'Basic {settings.PROXY_AUTH}'
                            })
        
        if as_bytes:
            return r.content
        else:
            return r.text

    @staticmethod 
    def _get_names(html: str) -> list:
        tags = RE_A_TAG.findall(html)

        names = []
        for match in tags:
            if not match[0].startswith('..'):
                names.append(match[0])

        return names

    @staticmethod
    @cache
    def get_dates() -> list:
        html = Proxy._request('')
        dates = [date[:-1] for date in Proxy._get_names(html)]
        return dates

    @staticmethod
    @cache
    def get_images(date: str) -> list:
        html = Proxy._request(f'{date}/')
        images = Proxy._get_names(html)
        return images

    @staticmethod
    def get_image(date: str, image: str) -> list:
        image = Proxy._request(f'{date}/{image}', as_bytes=True)
        image = base64.b64encode(image).decode('utf-8')
        return image
