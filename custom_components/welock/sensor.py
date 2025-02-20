"""."""

from welock_iot.const import SENSOR_BATTERY_KEY, SENSOR_RECORD_KEY
from welock_iot.models import DeviceType, WeLockDevice

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import WelockConfigEntry
from .const import WELOCK_DEVICE_DISCOVER
from .entity import WeLockEntity

SENSORS: dict[str, tuple[SensorEntityDescription, ...]] = {
    DeviceType.WELOCK.name: (
        SensorEntityDescription(
            key=SENSOR_BATTERY_KEY,
            translation_key="sensor.battery",
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
            icon="mdi:battery-60",
        ),
        SensorEntityDescription(
            key=SENSOR_RECORD_KEY,
            translation_key="sensor.record",
            icon="mdi:history",
        ),
    ),
    DeviceType.DOORS.name: (
        SensorEntityDescription(
            key=SENSOR_BATTERY_KEY,
            translation_key="sensor.battery",
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.BATTERY,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
            icon="mdi:battery-60",
        ),
    ),
    DeviceType.WIFIBOX3.name: (
        SensorEntityDescription(
            key=SENSOR_RECORD_KEY,
            translation_key="sensor.record",
            icon="mdi:history",
        ),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WelockConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the config entry."""

    hass_data = entry.runtime_data

    @callback
    def async_discover_device(device_list: list[str]) -> None:
        """Discover and add welock sensor."""
        entities: list[BatteryEntity] = []
        for device_id in device_list:
            device = hass_data.manager.device_map[device_id]
            if descriptions := SENSORS.get(device.device_type.name):
                for description in descriptions:
                    entities.append(BatteryEntity(device, description))
        async_add_entities(entities)

    entry.async_on_unload(
        async_dispatcher_connect(hass, WELOCK_DEVICE_DISCOVER, async_discover_device)
    )
    async_discover_device([*hass_data.manager.device_map])


class BatteryEntity(WeLockEntity, SensorEntity):
    """BatteryEntity or RecordEntity."""

    def __init__(
        self, device: WeLockDevice, description: SensorEntityDescription
    ) -> None:
        """Init ."""
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}_{description.key}"
        self._attr_name = f"{self.device.device_name} {description.key}"

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""

        key = self.entity_description.key
        if key == SENSOR_BATTERY_KEY:
            return self.device.status.get(
                key, None if self.device.battery == 0 else self.device.battery
            )
        if key == SENSOR_RECORD_KEY:
            return self.device.status.get(key)

        return None
