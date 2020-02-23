"""46Elks SMS notify component."""
import logging

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.components.elks import DATA_46ELKS
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
            ),
        )
    }
)


def get_service(hass, config, discovery_info=None):
    return ElksSMSNotificationService(
        hass.data[DATA_46ELKS], config[CONF_FROM_NUMBER]
    )


class ElksSMSNotificationService(BaseNotificationService):

    def __init__(self, elks_client, from_number):
        """Initialize the service."""
        self.client = elks_client
        self.from_number = from_number

    def send_message(self, message="", **kwargs):
        targets = kwargs.get(ATTR_TARGET)
        data = kwargs.get(ATTR_DATA) or {}
        elks_args = {"message": message, "sender": self.from_number}

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        if ATTR_IMAGE in data:
            elks_args[ATTR_IMAGE] = data[ATTR_IMAGE]
            # The sender argument doesn't work with mms
            del elks_args["sender"]
            for target in targets:
                self.client.send_mms(to=target, **elks_args)
        else:
            for target in targets:
                self.client.send_sms(to=target, **elks_args)



