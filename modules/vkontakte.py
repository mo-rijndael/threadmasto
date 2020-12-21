import vk

from exceptions import InvalidConfig
from publication import Publication, Attachment
from . import Source


def parse_attachment():
    ...


@Source.register("vk")
class VKSource(Source):
    token: str
    id: int
    api: vk.API

    def __init__(self, raw: dict):
        self.token = raw['token']
        self.api = vk.API(vk.Session(access_token=self.token), v=5.95)
        id_or_domain = raw['target']
        if isinstance(id_or_domain, str):
            target = self.api.utils.resolveScreenName(screen_name=id_or_domain)
            if target == {}:
                raise InvalidConfig("Target is not exists")
            if target['type'] == 'user':
                self.id = target['object_id']
            elif target['type'] == 'group':
                self.id = -target['object_id']
            else:
                raise InvalidConfig("Target must be user or group")
        else:
            self.id = id_or_domain

    def get(self, after_timestamp: float) -> list:
        posts = self.api.wall.get(owner_id=self.id, count=100, filter='owner')
        posts = filter(lambda p: p['date'] > after_timestamp, posts['items'])
        parsed = []
        for post in posts:
            text = post['text']
            parsed.append(Publication(text=text))
        return parsed
