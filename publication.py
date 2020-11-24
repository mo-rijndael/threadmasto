from typing import List, Dict, Any

from mastodon import Mastodon


class Attachment:
    link: str
    type: str

    def __init__(self, object_: Dict[str, Any]):
        ...

    def upload(self, api: Mastodon) -> str:
        ...


class Publication:
    formatted_text: str
    attachments: List[Attachment]

    def __init__(self):
        ...

    def publish(self, api: Mastodon):
        ...

    def split(self) -> List['Publication']:
        ...
