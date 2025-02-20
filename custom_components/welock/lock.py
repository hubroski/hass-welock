"""."""

import asyncio
from typing import Any

from welock_iot.const import LOCK_WELOCK_KEY
from welock_iot.manager import Resmanager
from welock_iot.models import DeviceType, WeLockDevice

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WelockConfigEntry
from .const import WELOCK_DEVICE_DISCOVER
from .entity import WeLockEntity

LOCKS: dict[str, tuple[LockEntityDescription, ...]] = {
    DeviceType.WELOCK.name: (
        LockEntityDescription(
            key=LOCK_WELOCK_KEY,
            translation_key="welocks",
            # icon="mdi:lock-open-variant-outline",
        ),
    )
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WelockConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up lock entry."""
    hass_data = entry.runtime_data

    @callback
    def async_discover_device(device_list: list[str]) -> None:
        """Discover and add a lock."""
        entities: list[UserLockEntity] = []
        for device_id in device_list:
            device = hass_data.manager.device_map[device_id]
            if descriptions := LOCKS.get(device.device_type.name):
                for description in descriptions:
                    entities.append(
                        UserLockEntity(device, description, hass_data.manager)
                    )
        async_add_entities(entities)

    entry.async_on_unload(
        async_dispatcher_connect(hass, WELOCK_DEVICE_DISCOVER, async_discover_device)
    )
    async_discover_device([*hass_data.manager.device_map])


class UserLockEntity(WeLockEntity, LockEntity):
    """WeLock Lock entity."""

    def __init__(
        self,
        device: WeLockDevice,
        description: LockEntityDescription,
        res_manager: Resmanager,
    ) -> None:
        """Init lock."""
        super().__init__(device)
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}_{description.key}"
        self._attr_name = f"{self.device.device_name} {description.key}"
        self._attr_is_locked = True
        self.res_manager = res_manager

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock all or specified locks. A code to lock the lock with may optionally be specified."""

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock all or specified locks. A code to unlock the lock with may optionally be specified."""

        state = await self.res_manager.unlock(self.device)
        if state:
            self._attr_is_locked = False
            self._attr_is_unlocking = True
        else:
            self._attr_is_unlocking = False
            self._attr_is_locked = True
        self.async_write_ha_state()
        if state:
            await self._handle_auto_lock()

    async def _handle_auto_lock(self):
        """Handle auto lock the lock delay 8seonds."""
        await asyncio.sleep(8)
        self._attr_is_unlocking = False
        self._attr_is_locked = True
        self.async_write_ha_state()
