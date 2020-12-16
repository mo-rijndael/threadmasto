from typing import List
from enum import IntEnum


class AttachmentType(IntEnum):
    AUDIO = 1
    PICTURE = 2
    VIDEO = 3
    CUSTOM = 4
    POLL = 5


class Attachment:
    link: str

    def __init__(self, link: str):
        ...


class Publication:
    formatted_text: str
    attachments: List[Attachment]

    def __init__(self):
        ...
