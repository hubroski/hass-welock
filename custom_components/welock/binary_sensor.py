"""WeLock device like door sensor."""

from welock_iot.const import BINARYSENSORS_DOOR_KEY
from welock_iot.models import DeviceType, WeLockDevice

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WelockConfigEntry
from .const import WELOCK_DEVICE_DISCOVER
from .entity import WeLockEntity

BINARYSENSORS: dict[str, tuple[BinarySensorEntityDescription, ...]] = {
    DeviceType.DOORS.name: (
        BinarySensorEntityDescription(
            key=BINARYSENSORS_DOOR_KEY,
            device_class=BinarySensorDeviceClass.DOOR,
            translation_key="sensor_open",
        ),
    )
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WelockConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all the sensors for the config entry."""
    hass_data = entry.runtime_data

    @callback
    def async_discover_device(device_list: list[str]) -> None:
        """Discover and add a door sensor."""
        entities: list[LockStateBinarySensorEntity] = []
        for device_id in device_list:
            device = hass_data.manager.device_map[device_id]
            if descriptions := BINARYSENSORS.get(device.device_type.name):
                for description in descriptions:
                    entities.append(LockStateBinarySensorEntity(device, description))
        async_add_entities(entities)

    entry.async_on_unload(
        async_dispatcher_connect(hass, WELOCK_DEVICE_DISCOVER, async_discover_device)
    )
    async_discover_device([*hass_data.manager.device_map])


class LockStateBinarySensorEntity(WeLockEntity, BinarySensorEntity):
    """Door sensor entity."""

    def __init__(
        self, device: WeLockDevice, description: BinarySensorEntityDescription
    ) -> None:
        """Init door sensor."""
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}_{description.key}"
        self._attr_name = f"{self.device.device_name} {description.key}"

    @property
    def is_on(self) -> bool:
        """Return the report data."""
        return self.device.status.get(self.entity_description.key)
