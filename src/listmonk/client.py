from __future__ import annotations

from base64 import b64encode

from klarient import (
    RequestsClient,
    RequestsOptions,
)
from listmonk.bounces.resources import BouncesResource
from listmonk.campaigns.resources import CampaignsResource
from listmonk.imports.resources import ImportResource
from listmonk.lists.resources import ListsResource
from listmonk.media.resources import MediaRootResource
from listmonk.public.resources import PublicResource
from listmonk.subscribers.resources import SubscribersResource
from listmonk.templates.resources import TemplatesResource
from listmonk.transactional.resources import TransactionalResource


class ListMonkClient(RequestsClient):
    """Synchronous typed client for the Listmonk REST API.

    The client exposes Listmonk resources as attributes such as ``subscribers``,
    ``lists``, ``campaigns``, and ``templates``. Network behavior is configured
    with ``options`` when timeout, proxy, or SSL behavior needs tuning.
    """

    bounces: BouncesResource
    campaigns: CampaignsResource
    imports: ImportResource
    lists: ListsResource
    media: MediaRootResource
    public: PublicResource
    subscribers: SubscribersResource
    templates: TemplatesResource
    tx: TransactionalResource

    def __init__(
            self,
            *,
            base_url: str,
            username: str | None = None,
            access_token: str | None = None,
            options: RequestsOptions | None = None,
    ) -> None:
        """Create a Listmonk client.

        ``base_url`` is the Listmonk server root, for example
        ``https://listmonk.example.com``. Provide ``username`` and
        ``access_token`` for HTTP Basic authentication. ``options`` configures
        network behavior without exposing transport internals.
        """
        configured_headers = {}
        if username is not None and access_token is not None:
            credentials = f"{username}:{access_token}".encode("utf-8")
            configured_headers.setdefault(
                "Authorization",
                f"Basic {b64encode(credentials).decode('ascii')}",
            )
        super().__init__(
            base_url=base_url,
            headers=configured_headers,
            options=options,
        )
        self.__bounces = self._bind_resource(BouncesResource, segment="api/bounces")
        self.__campaigns = self._bind_resource(
            CampaignsResource,
            segment="api/campaigns",
        )
        self.__imports = self._bind_resource(ImportResource, segment="api/import")
        self.__lists = self._bind_resource(ListsResource, segment="api/lists")
        self.__media = self._bind_resource(MediaRootResource, segment="api/media")
        self.__subscribers = self._bind_resource(
            SubscribersResource,
            segment="api/subscribers",
        )
        self.__templates = self._bind_resource(
            TemplatesResource,
            segment="api/templates",
        )
        self.__tx = self._bind_resource(TransactionalResource, segment="api/tx")
        self.__public = self._bind_resource(PublicResource, segment="api/public")

    @property
    def bounces(self) -> BouncesResource:
        """Bounces resource root."""
        return self.__bounces

    @property
    def campaigns(self) -> CampaignsResource:
        """Campaigns resource root."""
        return self.__campaigns

    @property
    def imports(self) -> ImportResource:
        """Imports resource root."""
        return self.__imports

    @property
    def lists(self) -> ListsResource:
        """Lists resource root."""
        return self.__lists

    @property
    def media(self) -> MediaRootResource:
        """Media resource root."""
        return self.__media

    @property
    def public(self) -> PublicResource:
        """Public subscription resource root."""
        return self.__public

    @property
    def subscribers(self) -> SubscribersResource:
        """Subscribers resource root."""
        return self.__subscribers

    @property
    def templates(self) -> TemplatesResource:
        """Templates resource root."""
        return self.__templates

    @property
    def tx(self) -> TransactionalResource:
        """Transactional email resource root."""
        return self.__tx
