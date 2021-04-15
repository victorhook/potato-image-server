from django.conf import settings
import requests
import re

RE_A_TAG: re.Pattern = re.compile('href="(.*)">(.*)<\/a>')


class Proxy:

    @staticmethod
    def _request(endpoint: str) -> str:
        r = requests.get(f'{settings.PROXY_HOST}/{endpoint}',
                        headers={
                            'Authorization': f'Basic {settings.PROXY_AUTH}'
                            })
        return r.text

    @staticmethod
    def get_dates() -> list:
        html = Proxy._request('')
        dates = RE_A_TAG.findall(html)

        refs = []
        names = []
        for match in dates:
            if not match[0].startswith('..'):
                refs.append(match[0])
                names.append(match[1][:-1])

        print(list(zip(refs, names)))

        return zip(refs, names)

    @staticmethod
    def get_images(date: str) -> list:
        html = Proxy._request(date)
        return []


if __name__ == '__main__':


    print(r.text)