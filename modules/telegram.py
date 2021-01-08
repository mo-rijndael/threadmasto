from typing import Tuple, List

from telegrambotapiwrapper import Api

from . import Destination
from exceptions import InvalidConfig
from publication import Publication, Poll, FileType, FileAttach


def smart_cut(text: str, max_len: int) -> Tuple[str, str]:
    index_of_space = text.rfind(' ', 0, max_len+1)
    if index_of_space == -1:
        cut_index = max_len
    else:
        cut_index = index_of_space
    return text[:cut_index], text[cut_index:]


def extract_head(post: Publication) -> tuple:
    if post.attachments:
        if len(post.plain_text) > 1024:
            head, tail = smart_cut(post.plain_text, 1024)
            head = Publication(head)
            tail = Publication(tail, post.attachments)
            return head, tail
        for index, attach in enumerate(post.attachments):
            if type(attach) is Poll:
                head = Publication(attachments=[attach])
                post.attachments.pop(index)
                if not post.plain_text and not post.attachments:
                    post = None
                return head, post
        return post, None


def split(post: Publication):
    posts = []
    splitting_now = post
    while True:
        head, tail = extract_head(splitting_now)
        posts.append(head)
        if tail is None:
            break
        else:
            splitting_now = tail
    return posts


@Destination.register("telegram")
class TelegramDest(Destination):
    api: Api
    target: str

    def __init__(self, raw: dict):
        try:
            token = raw['token']
            target = raw['target']
        except KeyError as e:
            raise InvalidConfig(f"Missing field {e.args[0]}")

        self.api = Api(token=token)
        self.target = target if target.startswith("@") else f"@{target}"

    def _serialise_attachments(self, attachments: List[FileAttach]):
        ...

    def _publish_poll(self, poll: Poll):
        ...

    def _publish_no_attach(self, post: Publication):
        ...

    def _publish_one_attach(self, post: Publication):
        ...

    def _publish_multi_attach(self, post: Publication):
        ...

    def publish(self, publication: Publication):
        ...
