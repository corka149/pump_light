import Config

config :pump_light,
  port: System.get_env("PORT", 4000),
  device: "pond_pump_149",
  light_on: "active",
  light_off: "inactive",
  light_pin: 18
