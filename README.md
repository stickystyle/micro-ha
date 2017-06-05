# micro-ha
Micropython code to interface with home-assistant.io via MQTT

Goals:
  - Provide a single binary that users can flash onto their MCU with basic functionality
  - Autodiscovery of HA and MQTT broker
  - Automatic configuration of entity in HA via https://home-assistant.io/docs/mqtt/discovery/
  - Basic sensors & inputs baked in. Motion, Temp, Input Button, LUX

Ideas taken from
  * https://github.com/davea/sonoff-mqtt
  * https://github.com/home-assistant/micropython-home-assistant
  * https://github.com/mirko/SonOTA
