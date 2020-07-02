"""46elks MMS notify component."""
import logging

import voluptuous as vol

from homeassistant.components.elks46 import DATA_46ELKS
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_FROM_NUMBER = "from_number"
ATTR_IMAGE = "image"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FROM_NUMBER): vol.All(
            cv.string,
            vol.Match(
                r"^\+?[1-9]\d{1,14}$|"
                r"^(?=.{1,11}$)[a-zA-Z0-9\s]*"
                r"[a-zA-Z][a-zA-Z0-9\s]*$"
                r"^(?:[a-zA-Z]+)\:?\+?[1-9]\d{1,14}$|"
                r"noreply"
            ),
        )
    }
)


def get_service(hass, config, discovery_info=None):
    """Get the notification service."""
    return elks46MMSNotificationService(
        hass.data[DATA_46ELKS], config[CONF_FROM_NUMBER]
    )


class elks46MMSNotificationService(BaseNotificationService):
    """elks46MMSNotificationService base on BaseNotificationService."""

    def __init__(self, elks46_client, from_number):
        """Initialize the service."""
        self.client = elks46_client
        self.from_number = from_number

    def send_message(self, message="", **kwargs):
        """Send MMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA) or {}
        elks46_args = {"message": message, ATTR_IMAGE: data[ATTR_IMAGE]}

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        if ATTR_IMAGE not in data:
            _LOGGER.info("Image is required for MMS")
            return

        for target in targets:
            self.client.send_mms(to=target, **elks46_args)
