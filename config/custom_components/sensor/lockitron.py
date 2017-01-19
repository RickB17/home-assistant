"""
Lockitron Sensor
by Rick Breidenstein
www.virtualrick.com

sample configuration.yaml entries
sensor:
  - platform: lockitron
    lock_name: 'VirtualLock'
    lock_uuid: 'YOURUUIDFORYOURLOCK'
    access_token: 'YOURACCESSTOKENHERE'
  - platform: lockitron
    lock_name: 'Some Other Door'
    lock_uuid: 'YOURUUIDFORYOURLOCK'
    access_token: 'YOURVERYLONGACCESSTOKENHERE'
"""
import logging
import voluptuous as vol
import requests

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_VALUE_TEMPLATE, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
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

    add_devices([LockitronSensor(lock_name, 'Unlocked', lock_uuid, access_token)])

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
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._lock_name

    @property
    def state(self):
        """Return the state of the sensor."""
        try:
            url = "https://api.lockitron.com/v2/locks/" + self._lock_uuid + "?access_token=" + self._access_token
            r = requests.get(url)
            resp = r.json()
            self._state = resp["state"]
        except:
            self._state = 'FAILED'
        return self._state

    def update(self):
        _LOGGER.info('Updating Lockitron state')
        """Return the state of the sensor."""
        try:
            url = "https://api.lockitron.com/v2/locks/" + self._lock_uuid + "?access_token=" + self._access_token
            r = requests.get(url)
            resp = r.json()
            self._state = resp["state"]
        except:
            self._state = 'FAILED'
        return self._state

class LockitronSensorData(object):
    """The class for handling the data retrieval."""

    def __init__(self, command):
        """Initialize the data object."""
        lock_uuid = config.get(CONF_LOCK_UUID)
        access_token = config.get(CONF_ACCESS_TOKEN)
        lock_name = config.get(CONF_LOCK_NAME)

    def update(self):
        """Get the latest data with a shell command."""
        _LOGGER.info('Updating Lockitron state for ' + self._lock_name)
        _LOGGER.info(self._lock_uuid)
        """Return the state of the sensor."""
        self._state = ''
        try:
            url = "https://api.lockitron.com/v2/locks/" + self._lock_uuid + "?access_token=" + self._access_token
            r = requests.get(url)
            resp = r.json()
            self._state = resp["state"]
        except:
            self._state = 'FAILED'
        return self._state
