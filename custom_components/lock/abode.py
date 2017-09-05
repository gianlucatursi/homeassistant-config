"""
This component provides HA lock support for Abode Security System.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/lock.abode/
"""
import logging

from custom_components.abode import AbodeDevice, DOMAIN
from homeassistant.components.lock import LockDevice


DEPENDENCIES = ['abode']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Abode lock devices."""
    import abodepy.helpers.constants as CONST

    data = hass.data[DOMAIN]

    devices = []
    for device in data.abode.get_devices(generic_type=CONST.TYPE_LOCK):
        if device.device_id not in data.exclude:
            devices.append(AbodeLock(data, device))

    data.devices.extend(devices)

    add_devices(devices)


class AbodeLock(AbodeDevice, LockDevice):
    """Representation of an Abode lock."""

    def __init__(self, data, device):
        """Initialize the Abode device."""
        AbodeDevice.__init__(self, data, device)

    def lock(self, **kwargs):
        """Lock the device."""
        self._device.lock()

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._device.unlock()

    @property
    def is_locked(self):
        """Return true if device is on."""
        return self._device.is_locked
