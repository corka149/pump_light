defmodule PumpLight.LightBuoy do

  use Task, restart: :permanent
  require Logger

  def start_link(_opts) do
    {:ok, socket} = :gen_udp.open(12347, [{:broadcast, true}])
    Task.start_link(__MODULE__, :blink, [socket])
  end

  def blink(socket) do
    Logger.debug("Beating")
    :gen_udp.send(socket, {255, 255, 255, 255}, 12346, "Beat")

    receive do
      _anything ->
        Logger.debug("Received a message but did not handle it")
    after 60_000 ->
      Logger.debug("Waiting")
    end
    blink(socket)
  end
end
