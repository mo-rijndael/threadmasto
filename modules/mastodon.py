from typing import Dict, Any, List

from mastodon import Mastodon

from publication import Publication
from . import Destination


@Destination.register('mastodon')
class MastodonDestination(Destination):
    api: Mastodon

    def __init__(self, raw: Dict[str, Any]):
        token = raw['token']
        base_url = raw['node']
        api = Mastodon(access_token=token, api_base_url=base_url)
        self.api = api

    @staticmethod
    def _split(post: Publication) -> List[Publication]:

    def publish(self, publication: Publication):
        pass
