"""Lockitron Sensor.
by Rick Breidenstein
www.virtualrick.com
"""

import logging
import voluptuous as vol
import requests

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_LOCK_UUID = 'lock_uuid'
CONF_ACCESS_TOKEN = 'access_token'
CONF_LOCK_NAME = 'lock_name'

SCAN_INTERVAL = 30

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LOCK_UUID): cv.string,
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
    vol.Required(CONF_LOCK_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Lockitron sensors."""
    lock_uuid = config.get(CONF_LOCK_UUID)
    access_token = config.get(CONF_ACCESS_TOKEN)
    lock_name = config.get(CONF_LOCK_NAME)

    add_devices(
        [LockitronSensor(lock_name, 'INIT', lock_uuid, access_token)]
        )


class LockitronSensor(Entity):
    """Representation of a Lockitron sensor."""

    def __init__(self, lock_name, state, lock_uuid, access_token):
        """Initialize the Lockitron sensor."""
        self._lock_name = lock_name
        self._state = state
        self._lock_uuid = lock_uuid
        self._access_token = access_token

    @property
    def should_poll(self):
        """Enable polling."""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._lock_name

    @property
    def state(self):
        """Return the state of the sensor."""
        url = (
            "https://api.lockitron.com/v2/locks/" + self._lock_uuid +
            "?access_token=" + self._access_token
            )
        req = requests.get(url)
        resp = req.json()
        self._state = resp["state"]
        return self._state

    def update(self):
        """Get the latest data with a shell command."""
        _LOGGER.info('Updating Lockitron state for ' + self._lock_name)
        url = (
            "https://api.lockitron.com/v2/locks/" + self._lock_uuid +
            "?access_token=" + self._access_token
            )
        req = requests.get(url)
        resp = req.json()
        self._state = resp["state"]
        return self._state


class LockitronSensorData(LockitronSensor):
    """The class for handling the data retrieval."""

    def update(self):
        """Get the latest data with a shell command."""
        _LOGGER.info('Updating Lockitron state for ' + self._lock_name)
        url = (
            "https://api.lockitron.com/v2/locks/" + self._lock_uuid +
            "?access_token=" + self._access_token
            )
        req = requests.get(url)
        resp = req.json()
        self._state = resp["state"]
        _LOGGER.info('Insdie Try ' + self._state)
        return self._state
