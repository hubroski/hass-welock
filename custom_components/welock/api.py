"""API for welock bound to Home Assistant OAuth."""

from aiohttp import ClientSession
from welock_iot.auth_token_manager import OauthTokenManager

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow


class ConfigEntryAuth(OauthTokenManager):
    """Provide welock authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        hass: HomeAssistant,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize auth."""
        self.hass = hass
        self._oauth_session = oauth_session
        super().__init__(websession)

    def access_token(self) -> str:
        """Return the access token."""
        return self._oauth_session.token["access_token"]

    async def check_and_refresh_token(self) -> str:
        """Check the token."""
        if not self._oauth_session.valid_token:
            await self._oauth_session.async_ensure_token_valid()
        return self.access_token()
