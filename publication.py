from typing import List


class Attachment:
    link: str

    def __init__(self, link: str):
        ...


class Publication:
    formatted_text: str
    attachments: List[Attachment]

    def __init__(self):
        ...
