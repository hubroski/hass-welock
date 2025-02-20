"""Base entity."""

from welock_iot.models import WeLockDevice

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, WELOCK_DEVICE_UPDATE


class WeLockEntity(Entity):
    """The base entity."""

    # _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, device: WeLockDevice) -> None:
        """."""
        self.device = device
        self._attr_unique_id = f"welock.{device.device_id}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.device.device_id)},
            manufacturer="WELOCK",
            name=self.device.device_name,
            model=self.device.model_show,
        )

    async def async_added_to_hass(self) -> None:
        """Call when entity is added to hass."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{WELOCK_DEVICE_UPDATE}_{self.device.device_id}",
                self.async_write_ha_state,
            )
        )
