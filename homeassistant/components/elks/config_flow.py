"""Config flow for sms integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "46Elks Webhook",
    {
        "elks_url": "https://46elks.com/products/virtual-numbers",
        "docs_url": "https://www.home-assistant.io/integrations"
    }
)