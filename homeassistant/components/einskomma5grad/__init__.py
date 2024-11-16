"""The 1KOMMA5GRAD integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .api.client import Client

PLATFORMS: list[Platform] = [Platform.SENSOR]

type ApiConfigEntry = ConfigEntry[Client]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ApiConfigEntry) -> bool:
    """Set up 1KOMMA5GRAD from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = entry

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    api_client = Client(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    await hass.async_add_executor_job(api_client.get_token)

    entry.runtime_data = api_client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ApiConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
