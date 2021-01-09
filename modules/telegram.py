from typing import Tuple, List

from telegrambotapiwrapper import Api, typelib

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
                if post.plain_text:
                    tail = Publication(attachments=[attach])
                    post.attachments.pop(index)
                    if not post.plain_text and not post.attachments:
                        post = None
                    return post, tail
                else:
                    return post, None

        attachments = {}
        for i in post.attachments:
            attachments.setdefault(i.type, []).append(i)
        if FileType.PICTURE in attachments:
            attachments[FileType.PICTURE].extend(attachments.get(FileType.VIDEO, []))
        attachments = list(attachments.values())
        head = Publication(post.plain_text, attachments.pop(0))
        if attachments:
            tail = Publication(attachments=attachments.pop(0))
        else:
            tail = None
        # господи прости меня за этот пиздец выше

        return head, tail


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

    @staticmethod
    def _serialise_attachments(attachments: List[FileAttach]):
        parsed = []
        for i in attachments:
            if i.type is FileType.PICTURE:
                i = typelib.InputMediaPhoto(type='photo', media=i.link)
            elif i.type is FileType.VIDEO:
                i = typelib.InputMediaVideo(type='video', media=i.link)
            elif i.type is FileType.AUDIO:
                i = typelib.InputMediaAudio(type='audio', media=i.link)
            elif i.type is FileType.CUSTOM:
                i = typelib.InputMediaDocument(type='document', media=i.link)
            parsed.append(i)
        return parsed

    def _publish_poll(self, poll: Poll):
        self.api.send_poll(chat_id=self.target,
                           question=poll.title,
                           options=poll.variants,
                           is_anonymous=True,
                           allows_multiple_answers=poll.multiple,
                           )

    def _publish_no_attach(self, post: Publication):
        self.api.send_message(chat_id=self.target, text=post.plain_text)

    def _publish_one_attach(self, post: Publication):
        attach = post.attachments[0]
        if type(attach) is Poll:
            self._publish_poll(attach)
        elif attach.type == FileType.PICTURE:
            self.api.send_photo(chat_id=self.target,
                                photo=attach.link or attach.fd,
                                caption=post.plain_text)
        elif attach.type == FileType.VIDEO:
            self.api.send_video(chat_id=self.target,
                                video=attach.link or attach.fd,
                                caption=post.plain_text)
        elif attach.type == FileType.AUDIO:
            self.api.send_audio(chat_id=self.target,
                                audio=attach.link or attach.fd,
                                caption=post.plain_text)
        elif attach.type == FileType.CUSTOM:
            self.api.send_document(chat_id=self.target,
                                   document=attach.link or attach.fd,
                                   caption=post.plain_text)

    def _publish_multi_attach(self, post: Publication):
        attachments = self._serialise_attachments(post.attachments)
        self.api.send_media_group(chat_id=self.target,
                                  media=attachments)

    def publish(self, publication: Publication):
        posts = split(publication)
        for i in posts:
            if not i.attachments:
                self._publish_no_attach(i)
            elif len(i.attachments) == 1:
                self._publish_one_attach(i)
            else:
                self._publish_multi_attach(i)
