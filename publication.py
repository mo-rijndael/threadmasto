from typing import List, Dict, Any

class Attachment:
    link: str
    type: str

    def __init__(self, object_: Dict[str, Any]):
        ...


class Publication:
    formatted_text: str
    attachments: List[Attachment]

    def __init__(self):
        ...
