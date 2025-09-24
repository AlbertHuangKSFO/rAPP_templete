import os
from urllib.parse import urljoin
from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client
from .config import get_config

class OAuthManager:
    def __init__(self):
        self._async_client = None
        self._sync_client = None
        self._config = get_config()
        self._token_endpoint = urljoin(self._config.get("iam_base_url"), "/auth/realms/master/protocol/openid-connect/token")
        self._cert_path = os.path.join("/", self._config.get("ca_cert_file_path"), self._config.get("ca_cert_file_name"))

    def get_sync_client(self) -> OAuth2Client:
        if not self._sync_client:
            self._sync_client = OAuth2Client(
                client_id=self._config.get("iam_client_id"),
                client_secret=self._config.get("iam_client_secret"),
                scope="openid",
                token_endpoint=self._token_endpoint,
                verify=self._cert_path,
            )
            self._sync_client.fetch_token()
        return self._sync_client

    async def get_async_client(self) -> AsyncOAuth2Client:
        if not self._async_client:
            self._async_client = AsyncOAuth2Client(
                client_id=self._config.get("iam_client_id"),
                client_secret=self._config.get("iam_client_secret"),
                scope="openid",
                token_endpoint=self._token_endpoint,
                verify=self._cert_path,
            )
            await self._async_client.fetch_token()
        return self._async_client

    async def close(self):
        if self._async_client:
            await self._async_client.aclose()
        if self._sync_client:
            self._sync_client.close()

oauth_manager = OAuthManager()
