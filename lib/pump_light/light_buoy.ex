defmodule PumpLight.LightBuoy do

  use Task, restart: :permanent

  def start_link(_opts) do
    {:ok, socket} = :gen_udp.open(12347, [{:broadcast, true}])
    Task.start_link(__MODULE__, :blink, [socket])
  end

  def blink(socket) do
    :gen_udp.send(socket, {255, 255, 255, 255}, 12346, "Beat")

    receive do
      _anything ->
        blink(socket)
    after 60_000 ->
      blink(socket)
    end
  end

end
