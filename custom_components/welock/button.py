"""."""

from welock_iot.const import BUTTON_WIFIBOX_KEY
from welock_iot.manager import Resmanager
from welock_iot.models import DeviceType, WeLockDevice

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WelockConfigEntry
from .const import WELOCK_DEVICE_DISCOVER
from .entity import WeLockEntity

BUTTONS: dict[str, tuple[ButtonEntityDescription, ...]] = {
    DeviceType.WIFIBOX3.name: (
        ButtonEntityDescription(
            key=BUTTON_WIFIBOX_KEY,
            translation_key="button",
        ),
    )
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WelockConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all the buttons for the config entry."""
    hass_data = entry.runtime_data

    @callback
    def async_discover_device(device_list: list[str]) -> None:
        """Discover and add a button."""
        entities: list[WeLockButtonEntity] = []
        for device_id in device_list:
            device = hass_data.manager.device_map[device_id]
            if descriptions := BUTTONS.get(device.device_type.name):
                for description in descriptions:
                    entities.append(
                        WeLockButtonEntity(device, description, hass_data.manager)
                    )
        async_add_entities(entities)

    entry.async_on_unload(
        async_dispatcher_connect(hass, WELOCK_DEVICE_DISCOVER, async_discover_device)
    )
    async_discover_device([*hass_data.manager.device_map])


class WeLockButtonEntity(WeLockEntity, ButtonEntity):
    """For the wifibox3 button."""

    def __init__(
        self,
        device: WeLockDevice,
        description: ButtonEntityDescription,
        res_manager: Resmanager,
    ) -> None:
        """Init WeLock button like wifibox3 remote control."""
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}_{description.key}"
        self.res_manager = res_manager
        self._attr_name = f"{self.device.device_name} {description.key}"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.res_manager.remote_control(self.device)
