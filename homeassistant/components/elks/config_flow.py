"""Config flow for sms integration."""
import logging

from homeassistant.helpers import config_entry_flow

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)


config_entry_flow.register_webhook_flow(
    DOMAIN,
    "46Elks Webhook",
    {
        "elks_url": "https://46elks.com/products/virtual-numbers",
        "docs_url": "https://www.home-assistant.io/integrations",
    },
)
