"""The 46elks hub integration."""
import logging

from elks_sdk import Elk

from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_USER_ID = "user_id"
CONF_API_PASSWORD = "api_password"

DATA_46ELKS = DOMAIN
RECEIVED_DATA = f"{DOMAIN}_data_received"


async def async_setup(hass, config):
    """Set up the 46Elks component."""
    if DOMAIN not in config:
        _LOGGER.warning("Couldn't find domain in config file")
        return True

    conf = config[DOMAIN]
    hass.data[DATA_46ELKS] = Elk(conf.get(CONF_USER_ID), conf.get(CONF_API_PASSWORD))
    return True


async def handle_webhook(hass, webhook_id, request):
    """Handle incoming webhook from 46elks for inbound messages and calls."""
    data = dict(await request.post())
    data["webhook_id"] = webhook_id
    hass.bus.async_fire(RECEIVED_DATA, dict(data))

    return data


async def async_setup_entry(hass, entry):
    """Configure based on config entry."""
    hass.components.webhook.async_register(
        DOMAIN, "46elks", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.components.webhook.async_unregister(entry.data[CONF_WEBHOOK_ID])
    return True


# pylint: disable=invalid-name
async_remove_entry = config_entry_flow.webhook_async_remove_entry
