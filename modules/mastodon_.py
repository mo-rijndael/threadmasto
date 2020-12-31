from typing import Dict, Any, List, Tuple

from mastodon import Mastodon
import requests

from publication import Publication, Poll, FileAttach, FileType
from . import Destination


def smart_cut(text: str, max_len: int) -> Tuple[str, str]:
    index_of_space = text.rfind(' ', 0, max_len+1)
    if index_of_space == -1:
        cut_index = max_len
    else:
        cut_index = index_of_space
    return text[:cut_index], text[cut_index:]


def extract_head(post: Publication) -> Tuple:
    if len(post.plain_text) > 500:
        (head, tail) = smart_cut(post.plain_text, 500-len(' ->'))
        head = Publication(head)
        tail = Publication(tail, post.attachments)
        return head, tail
    if len(post.attachments) > 4:
        head = post.attachments[:4]
        tail = post.attachments[4:]
        head = Publication(post.plain_text, head)
        tail = Publication(attachments=tail)
        return head, tail
    for index, attach in enumerate(post.attachments):
        if type(attach) is Poll:
            head = Publication(attachments=[attach])
            post.attachments.pop(index)
            if not post.plain_text and not post.attachments:
                post = None
            return head, post
    return post, None


def split(post: Publication) -> List[Publication]:
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


@Destination.register('mastodon')
class MastodonDestination(Destination):
    api: Mastodon

    def __init__(self, raw: Dict[str, Any]):
        token = raw['token']
        base_url = raw['node']
        api = Mastodon(access_token=token, api_base_url=base_url)
        self.api = api

    def _upload_attachment(self, attach: FileAttach):
        req = requests.post(f"{self.api.api_base_url}/api/v1/media",
                            headers={"Authorization":
                                     f"Bearer {self.api.access_token}"},
                            files={'file': attach.fd}
                            )
        if req.ok:
            return req.json()

    def _publish_part(self, post: Publication, reply_to=None)\
            -> Dict[str, Any]:
        if post.attachments and type(post.attachments[0]) is Poll:
            raw: Poll = post.attachments[0]
            poll = self.api.make_poll(raw.variants, multiple=raw.is_multiple, expires_in=60*60*24*30)  # one month
            published = self.api.status_post(raw.title,
                                             poll=poll,
                                             in_reply_to_id=reply_to)
        else:
            uploaded_ids = []
            for i in post.attachments:
                if i.type == FileType.CUSTOM:
                    post.plain_text += '\n' + i.link if i.link else '[BROKEN ATTACH]'
                uploaded = self._upload_attachment(i)
                if uploaded:
                    uploaded_ids.append(uploaded)
            published = self.api.status_post(post.plain_text,
                                             media_ids=uploaded_ids,
                                             in_reply_to_id=reply_to)
        return published

    def publish(self, post: Publication):
        posts = split(post)
        current_id = self._publish_part(posts.pop(0))

        for p in posts:
            current_id = self._publish_part(p, current_id)
