defmodule PumpLight do
  @moduledoc """
  Handles the switching of the light
  """

  use GenServer

  ### Server

  def init(state) do
    {:ok, state}
  end

  def handle_cast({device, inc_state}, {old_light_state, gpio} = _state) do
    expected_device = device()

    light_state = case device do
      ^expected_device ->
        toggle_light(gpio, inc_state, old_light_state)
      _ ->
        old_light_state
    end

    {light_state, gpio}
  end

  ### Client

  def start_link(state \\ {:light_off, nil}) do
    state = case state do
      {:light_off, nil} ->
        Circuits.GPIO.open(output_pin(), :output, initial_value: 0)
      {:light_on, nil} ->
        Circuits.GPIO.open(output_pin(), :output, initial_value: 1)
      state ->
        state
    end

    GenServer.start_link(__MODULE__, {state}, name: __MODULE__)
  end

  def switch_light(device, state) do
    GenServer.cast(__MODULE__, {:switch_light, device, state})
  end

  ### Private

  defp output_pin do
    Application.get_env(:pump_light, :light_pin, 18)
  end

  defp device, do: Application.get_env(:pump_light, :device)

  defp get_states do
    {
      Application.get_env(:pump_light, :light_off),
      Application.get_env(:pump_light, :light_on)
    }
  end

  defp toggle_light(gpio, inc_state, old_state) do
    {light_off, light_on} = get_states()

    case inc_state do
      ^light_off ->
        Circuits.GPIO.write(gpio, 0)
        :light_off
      ^light_on ->
        Circuits.GPIO.write(gpio, 1)
        :light_on
      _ ->
        old_state
    end
  end
end
