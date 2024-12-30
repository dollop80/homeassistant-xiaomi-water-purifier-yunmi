"""Support for Xiaomi water purifier (Yunmi)."""
import math
import logging

from homeassistant.const import UnitOfTemperature
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, )
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
from miio import Device, DeviceException
from homeassistant import config_entries

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'water_purifier_yunmi'

RUN_STATUS = {'name': 'Run status', 'key': 'run_status'}
F1_REMAINING = {'name': 'PPC Filter', 'key': 'f1f', 'days_key': 'f1d'}
F2_REMAINING = {'name': 'RO Filter', 'key': 'f2f', 'days_key': 'f2d'}
F3_REMAINING = {'name': 'CB Filter', 'key': 'f3f', 'days_key': 'f3d'}
TDS_IN = {'name': 'TDS in', 'key': 'tds_in'}
TDS_OUT = {'name': 'TDS out', 'key': 'tds_out'}
TEMPERATURE = {'name': 'Temperature', 'key': 'temperature'}
RINSE = {'name': 'Rinse', 'key': 'rinse'}
WATER_USED = {'name': 'Water used', 'key': 'water_used'}
WATER_PURIFIED = {'name': 'Water purified', 'key': 'water_purified'}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for Yunmi Xiaomi water purifier."""
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing Yunmi Xiaomi water purifier with host %s (token %s...)", host, token[:5])

    devices = []
    try:
        device = Device(host, token)
        waterPurifier = XiaomiWaterPurifier(device, name)
        devices.append(waterPurifier)
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RUN_STATUS))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, F1_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, F2_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, F3_REMAINING))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TDS_IN))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TDS_OUT))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, TEMPERATURE))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, RINSE))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, WATER_USED))
        devices.append(XiaomiWaterPurifierSensor(waterPurifier, WATER_PURIFIED))
    except DeviceException:
        _LOGGER.exception('Fail to setup Yunmi Xiaomi water purifier')
        raise PlatformNotReady

    add_devices(devices)

class XiaomiWaterPurifierSensor(Entity):
    """Representation of a XiaomiWaterPurifierSensor."""

    def __init__(self, waterPurifier, data_key):
        """Initialize the XiaomiWaterPurifierSensor."""
        self._state = None
        self._data = None
        self._waterPurifier = waterPurifier
        self._data_key = data_key
        self.parse_data()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._data_key['name']

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._data_key['key'] is TDS_IN['key'] or \
           self._data_key['key'] is TDS_OUT['key']:
            return 'mdi:water'
        if self._data_key['key'] is TEMPERATURE['key']:
            return 'mdi:thermometer'
        if self._data_key['key'] is RINSE['key'] or \
           self._data_key['key'] is RUN_STATUS['key']:
            return 'mdi:replay'   
        else:
            return 'mdi:filter-outline'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        if self._data_key['key'] is TDS_IN['key'] or \
           self._data_key['key'] is TDS_OUT['key']:
            return 'TDS'
        if self._data_key['key'] is WATER_USED['key'] or \
           self._data_key['key'] is WATER_PURIFIED['key']:
            return 'L'
        if self._data_key['key'] is TEMPERATURE['key']:
            return UnitOfTemperature.CELSIUS
        if self._data_key['key'] is RINSE['key'] or \
           self._data_key['key'] is RUN_STATUS['key']:
            return ''         
        return '%'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}

        if self._data_key['key'] is F1_REMAINING['key'] or \
           self._data_key['key'] is F2_REMAINING['key'] or \
           self._data_key['key'] is F3_REMAINING['key']:
            attrs[self._data_key['name']] = '{} days remaining'.format(self._data[self._data_key['days_key']])

        return attrs

    def parse_data(self):
        if self._waterPurifier._data:
            self._data = self._waterPurifier._data
            self._state = self._data[self._data_key['key']]

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()

class XiaomiWaterPurifier(Entity):
    """Representation of a XiaomiWaterPurifier."""

    def __init__(self, device, name):
        """Initialize the XiaomiWaterPurifier."""
        self._state = None
        self._device = device
        self._name = name
        self.parse_data()

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:water'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return 'TDS'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def hidden(self):
        """Return True if the entity should be hidden from UIs."""
        return True

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}
        attrs[RUN_STATUS['name']] = '{}'.format(self._data[RUN_STATUS['key']])
        attrs[TDS_IN['name']] = '{} TDS'.format(self._data[TDS_IN['key']])
        attrs[TDS_OUT['name']] = '{} TDS'.format(self._data[TDS_OUT['key']])
        attrs[F1_REMAINING['name']] = '{} %'.format(self._data[F1_REMAINING['key']])
        attrs[F2_REMAINING['name']] = '{} %'.format(self._data[F2_REMAINING['key']])
        attrs[F3_REMAINING['name']] = '{} %'.format(self._data[F3_REMAINING['key']])
        attrs[TEMPERATURE['name']] = '{} u2103'.format(self._data[TEMPERATURE['key']])
        attrs[RINSE['name']] = '{}'.format(self._data[RINSE['key']])
        attrs[WATER_USED['name']] = '{}'.format(self._data[WATER_USED['key']])
        attrs[WATER_PURIFIED['name']] = '{}'.format(self._data[WATER_PURIFIED['key']])
        return attrs

    def parse_data(self):
        """Parse data."""
        try:
            data = {}
            status = self._device.get_properties(["all"])

            data[RUN_STATUS['key']] = status[0]
            data[TDS_IN['key']] = status[9]
            data[TDS_OUT['key']] = status[10]
            
            f1f = int(100 - (status[3]/status[1]) * 100)
            f1d = int(100 - (status[4]/status[2]) * 100)
            data[F1_REMAINING['days_key']] = int((status[2] - status[4])/24)
            data[F1_REMAINING['key']] = min([f1f, f1d])
            
            f2f = int(100 - (status[7]/status[5]) * 100)
            f2d = int(100 - (status[8]/status[6]) * 100)
            data[F2_REMAINING['days_key']] = int((status[6] - status[8])/24)
            data[F2_REMAINING['key']] = min([f2f, f2d])

            
            f3f = int(100 - (status[16]/status[14]) * 100)
            f3d = int(100 - (status[17]/status[15]) * 100)
            data[F3_REMAINING['days_key']] = int((status[15] - status[17])/24)
            data[F3_REMAINING['key']] = min([f3f, f3d])
            
            data[TEMPERATURE['key']] = status[12]
            data[RINSE['key']] = status[11]

            data[WATER_USED['key']] = status[3]
            data[WATER_PURIFIED['key']] = int((status[7]+status[16])/2)

            self._data = data
            self._state = self._data[TDS_OUT['key']]
        except DeviceException:
            self._data = None
            self._state = None
            raise PlatformNotReady

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()
