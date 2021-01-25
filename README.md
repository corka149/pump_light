# pump_light

Firmware for a device that turn off/on signal lights.

## Build

Insert a SD card and run the following steps:
  * `export MIX_TARGET=rpi0`
  * `export WLAN_SSID=******`
  * `export WLAN_PASSWORD=******`
  * `mix firmware`
  * `mix firmware.burn`

## Config

Change rpi0.exs:
```elixir
config :pump_light,
  device: "pond_pump_149",
  light_pin: 18
```
