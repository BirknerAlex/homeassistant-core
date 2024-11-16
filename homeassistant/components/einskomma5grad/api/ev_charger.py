from enum import Enum

from .client import Client


class ChargingMode(Enum):
    """Enum representing different charging modes for the EV charger."""

    SMART_CHARGE = "SMART_CHARGE"
    QUICK_CHARGE = "QUICK_CHARGE"
    SOLAR_CHARGE = "SOLAR_CHARGE"


class EVCharger:
    """Class representing an EV charger."""

    def __init__(self, api: Client, system, data: dict) -> None:
        """Initialize the EVCharger with the given API client, system, and data."""

        self._api = api
        self._data = data

    def id(self) -> str:
        return self._data["id"]

    def charging_mode(self) -> ChargingMode:
        return ChargingMode(self._data["chargingMode"])

    def set_charging_mode(self, mode: ChargingMode):
        # TODO: Implement PATCH https://heartbeat.1komma5grad.com/api/v1/systems/5618a57f-0b6d-4e07-8694-4fc87a7f22d1/devices/evs/2b4f771c-be18-4d18-8bad-4f00a20441d7
        #
        pass
