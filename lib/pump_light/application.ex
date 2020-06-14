defmodule PumpLight.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  def start(_type, _args) do
    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: PumpLight.Supervisor]

    children =
      [
        # Children for all targets
        # Starts a worker by calling: PumpLight.Worker.start_link(arg)
        # {PumpLight.Worker, arg},
      ] ++ children(target())

    Supervisor.start_link(children, opts)
  end

  # List all child processes to be supervised
  def children(:host) do
    [
      cowboy_plug()
    ]
  end

  def children(_target) do
    [
      cowboy_plug()
    ]
  end

  def target() do
    Application.get_env(:pump_light, :target)
  end

  defp cowboy_plug() do
    {Plug.Cowboy,
     scheme: :http,
     plug: PumpLight.HttpInterface,
     options: [port: Application.get_env(:pump_light, :port, 4000)]}
  end
end
