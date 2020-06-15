defmodule PumpLight.HttpInterface do
  @moduledoc """
  Interface for the pond pump device
  """
  import Plug.Conn

  require Logger

  def init(options) do
    Logger.info(
      "Init http interface. Listens on port 4000"
    )

    options
  end

  def call(%{request_path: "/v1/device/" <> device_state} = conn, _opts) do
    [device, state] = String.split(device_state, "/")
    Logger.info("Switch state of '#{device}' to #{state}")
    PumpLight.switch_light(device, state)

    conn
    |> put_resp_content_type("text/plain")
    |> send_resp(200, "Status changed")
  end

  def call(conn, _ops) do
    conn
    |> put_resp_content_type("text/plain")
    |> send_resp(404, "Not found")
  end
end
