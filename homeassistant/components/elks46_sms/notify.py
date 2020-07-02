"""46elks SMS notify component."""
import logging

import voluptuous as vol

from homeassistant.components.elks46 import DATA_46ELKS
from homeassistant.components.notify import (
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_FROM_NUMBER = "from_number"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FROM_NUMBER): vol.All(
            cv.string,
            vol.Match(
                r"^\+?[1-9]\d{1,14}$|"
                r"^(?=.{1,11}$)[a-zA-Z0-9\s]*"
                r"[a-zA-Z][a-zA-Z0-9\s]*$"
                r"^(?:[a-zA-Z]+)\:?\+?[1-9]\d{1,14}$|"
            ),
        )
    }
)


def get_service(hass, config, discovery_info=None):
    """Get the notification service."""
    return elks46SMSNotificationService(
        hass.data[DATA_46ELKS], config[CONF_FROM_NUMBER]
    )


class elks46SMSNotificationService(BaseNotificationService):
    """elks46SMSNotificationService base on BaseNotificationService."""

    def __init__(self, elks_client, from_number):
        """Initialize the service."""
        self.client = elks_client
        # Check that the from_number follows the limitations
        self.from_number = from_number

    def send_message(self, message="", **kwargs):
        """Send SMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)
        elks_args = {"message": message, "sender": self.from_number}

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        for target in targets:
            self.client.send_sms(to=target, **elks_args)
