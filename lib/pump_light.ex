defmodule PumpLight do
  @moduledoc """
  Handles the switching of the light
  """

  use GenServer

  require Logger

  ### Server

  def init(state) do
    {:ok, state}
  end

  def handle_cast({:switch_light, device, inc_state}, {old_light_state, gpio} = _state) do
    expected_device = device()

    light_state =
      case device do
        ^expected_device ->
          toggle_light(gpio, inc_state, old_light_state)

        _ ->
          Logger.warn("Unkown device '#{device}'. Expected '#{expected_device}'!")
          old_light_state
      end

    {:noreply, {light_state, gpio}}
  end

  ### Client

  def start_link(_ops) do
    {:ok, gpio} = Circuits.GPIO.open(output_pin(), :output, initial_value: 0)

    GenServer.start_link(__MODULE__, {:light_off, gpio}, name: __MODULE__)
  end

  def switch_light(device, state) do
    GenServer.cast(__MODULE__, {:switch_light, device, state})
  end

  ### Private

  defp output_pin do
    Application.get_env(:pump_light, :light_pin, 18)
  end

  defp device, do: Application.get_env(:pump_light, :device)

  defp toggle_light(gpio, "inactive", _old_state) do
    Circuits.GPIO.write(gpio, 0)
    Logger.info("Will turn off the light")
    :light_off
  end

  defp toggle_light(gpio, "active", _old_state) do
    Circuits.GPIO.write(gpio, 1)
    Logger.info("Will turn on the light")
    :light_on
  end

  defp toggle_light(_gpio, unkown_state, old_state) do
    Logger.info("Unkown state '#{unkown_state}'")
    old_state
  end
end
