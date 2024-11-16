import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .api.systems import Systems
from .api.client import Client

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the 1KOMMA5GRAD sensor platform."""
    api_client = entry.runtime_data

    systems = Systems(api_client)
    systems = await hass.async_add_executor_job(systems.get_systems)
    for system in systems:
        async_add_entities([EnergyPriceSensor(api_client, system.id())], True)


class EnergyPriceSensor(SensorEntity):
    """Representation of an Energy Price Sensor."""

    def __init__(self, api_client, system_id):
        """Initialize the sensor."""
        self._api_client = api_client
        self._system_id = system_id
        self._name = f"Energy Price {system_id}"
        self._state = None
        self._unit_of_measurement = "EUR/kWh"
        self._prices = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    async def async_update(self):
        """Fetch new state data for the sensor."""
        systems = Systems(self._api_client)

        system = await self.hass.async_add_executor_job(
            systems.get_system, self._system_id
        )

        prices = await self.hass.async_add_executor_job(
            system.get_prices,
            dt_util.start_of_local_day(),
            dt_util.now(),
        )

        self._prices = {
            dt_util.parse_datetime(k): v["price"] / 100 for k, v in prices.items()
        }

        current_time = dt_util.now().replace(minute=0, second=0, microsecond=0)
        self._state = self._prices.get(current_time, None)
