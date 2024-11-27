from enum import Enum


class AccessModeState(Enum):
    """
    Related to Node: ADSModule.Network.AccessMode
    """

    via_target = 0
    direct_controller = 10
    bypass_controller = 20


class ADSModeState(Enum):
    """
    Related to Node: ADSModule.ADS.Mode
    """

    not_set = 0
    controller = 10
    hybrid = 20
    target = 30
    stand_alone = 100


class AMPDownloadMirrorState(Enum):
    """
    Related to Node: ADSModule.ADS.DownloadMirror
    """

    us_central = "[Automatic]"
    eu_west = ""
    us_central_texas = "US Central - Texas"


class AMPInstanceState(Enum):
    """
    Represents the state of an Instance and or Application inside an Instance.

    """

    undefined = -1
    stopped = 0
    pre_start = 5
    configuring = 7  # the server is performing some first-time-start configuration.
    starting = 10
    ready = 20
    restarting = 30  # server is in the middle of stopping, but once shutdown has finished it will automatically restart.
    stopping = 40
    preparing_for_sleep = 45
    sleeping = 50  # the application should be able to be resumed quickly if using this state. otherwise use stopped.
    waiting = 60  # the application is waiting for some external service/application to respond/become available.
    installing = 70
    updating = 75
    awaiting_user_input = (
        80  # used during installation, means that some user input is required to complete setup (authentication etc).
    )
    failed = 100
    suspended = 200
    maintenance = 250
    indeterminate = 999  # The state is unknown, or doesn't apply (for modules that don't start an external process)


class AMPTheme(Enum):
    """
    Related to Node: Core.AMP.Theme
    """

    aura = "Aura"
    black = "Black"
    tenth_anniversary = "TenthAnniversary"
    to_boldly_go = "ToBoldlyGo"
    default = "default"


class ApplicationUpdatesState(Enum):
    """
    Related to Node: steamcmdplugin.SteamUpdateSettings.UpdateCheckMethod
    """

    by_timestamp = 0
    by_build_id = 1


class AppStartupModeState(Enum):
    """
    Related to Node: Core.AMP.AppStartupMode
    """

    do_nothing = 0
    update = 1
    start = 2
    update_and_start = 3
    unk = 16
    unk2 = 32


class ContainerMemoryPolicyState(Enum):
    not_specified = 0
    reserve = 100
    restrict = 200


class DefaultIPBindingState(Enum):
    """
    Related to Node: ADSModule.Network.DockerExternalIPBinding, ADSModule.Network.DefaultAppIPBinding, ADSModule.Network.DefaultIPBinding
    """

    ipv4_loopback = "127.0.0.1"
    enp42s0 = "192.168.4.50"
    any_ipv4_address = "0.0.0.0"
    any_ipv6_address = "::"


class LoggingLevelState(Enum):
    """
    Related to Node: Core.Monitoring.LogLevel
    """

    debug = 0
    info = 10
    chat = 11
    notice = 20
    warning = 30
    error = 40
    activity = 5
    fatal = 50
    event = 7
    audit = 8


class PortAssignmentState(Enum):
    """
    Related to Node: ADSModule.Network.PortAssignment
    """

    include_allowed_ports_only = 0
    allow_all_except_excluded = 1


class PostCreateActionsState(Enum):
    """
    The action the Instance will take after creation. Used in dataclass parameters.

    """

    do_nothing = 0
    start_instance = 1
    start_and_update = 2
    full_startup = 3
    every_time = 16


class PostCreateState(Enum):
    """
    Represents the state of the API call `ADSModule/DeployTemplate`
    Related to Node: ADSModule.Defaults.DefaultPostCreate

    """

    do_nothing = 0
    update_once = 1
    update_always = 2
    update_and_start_once = 3
    update_and_start_always = 4
    start_always = 5


class ReleaseStreamState(Enum):
    """
    Related to Node: ADSModule.Defaults.DefaultReleaseStream
    """

    lts = 5
    mainline = 10
    preview = 15
    development = 20


class TwoFactoryModeState(Enum):
    """
    Related to Node: Core.Security.TwoFactorMode
    """

    optional = 0
    required = 1
