"""46Elks Call platform for notify component."""
import logging

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TARGET,
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.components.elks import DATA_46ELKS
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_FROM_NUMBER = "from_number"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FROM_NUMBER): vol.All(
            cv.string, vol.Match(r"^\+?[1-9]\d{1,14}$")
        )
    }
)


def get_service(hass, config, discovery_info=None):
    """Get the Elks Call notification service."""
    return ElksCallNotificationService(
        hass.data[DATA_46ELKS], config[CONF_FROM_NUMBER]
    )


class ElksCallNotificationService(BaseNotificationService):

    def __init__(self, elks_sdk, from_number):
        """Initialize the service."""
        self.client = elks_sdk
        self.from_number = from_number

    # Name has to be send_message cause of BaseNotificationService
    def send_message(self, message="", **kwargs):
        """Send SMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA) or {}
        elks_args = {"sender": self.from_number}

        if "voice_start" in data:
            elks_args["voice_start"] = data["voice_start"]

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        for target in targets:
            self.client.make_call(
                to=target, **elks_args
            )