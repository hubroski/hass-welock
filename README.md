## hass-welock

Home Assistant integration for welock based locks and wifibox.

### Overview
This integration uses the Welock Cloud and Wifibox to communicate with your lock. It supports the following features:

- Unlocking
- Lock battery level
- List records history

### Requirements

1. A WeLock based PCB,TOUCH,PBL ...
1. A wifibox/wifbox3 ...
1. The lock and wifibox are each already bound in the welock app.

### Setup via HACS (Home Assistant Community Store)
> [!IMPORTANT]
> Installation directly through HACS is not yet available because the integration is not yet official included into HACS. This process will take some time.

1. Find clientID and clientSecret via the home assistant icon on the left menu page in the welock app.
1. Install the extension [via HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=hzjchina&repository=hass-welock&category=integration) and restart Home Assistant.
<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=hzjchina&repository=hass-welock&category=Integration" target="_blank"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store." width="" height=""></a>