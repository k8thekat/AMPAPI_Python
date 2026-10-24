"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from enum import Enum, StrEnum

__all__ = (
    "ADSModeState",
    "AccessModeState",
    "AppStartupModeState",
    "IfOperators",
    "InstanceState",
    "MailPriority",
    "Module",
    "PostCreateState",
)


class AccessModeState(Enum):
    """Related to Node: ADSModule.Network.AccessMode"""

    via_target = 0
    direct_controller = 10
    bypass_controller = 20


class ADSModeState(Enum):
    """Related to Node: ADSModule.ADS.Mode"""

    not_set = 0
    controller = 10
    hybrid = 20
    target = 30
    stand_alone = 100


class AMPDownloadMirrorState(Enum):
    """Related to Node: ADSModule.ADS.DownloadMirror"""

    us_central = "[Automatic]"
    eu_west = ""
    us_central_texas = "US Central - Texas"


class AMPTheme(Enum):
    """Related to Node: Core.AMP.Theme"""

    aura = "Aura"
    black = "Black"
    tenth_anniversary = "TenthAnniversary"
    to_boldly_go = "ToBoldlyGo"
    default = "default"


class ApplicationUpdatesState(Enum):
    """Related to Node: steamcmdplugin.SteamUpdateSettings.UpdateCheckMethod"""

    by_timestamp = 0
    by_build_id = 1


class AppStartupModeState(Enum):
    """Related to Node: Core.AMP.AppStartupMode"""

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
    """Related to Node: ADSModule.Network.DockerExternalIPBinding, ADSModule.Network.DefaultAppIPBinding,
    ADSModule.Network.DefaultIPBinding
    """

    ipv4_loopback = "127.0.0.1"
    enp42s0 = "192.168.4.50"
    any_ipv4_address = "0.0.0.0"  # noqa: S104
    any_ipv6_address = "::"


class IfOperators(Enum):
    """The comparison a task's `CommonCorePlugin.IfCondition` and `CommonCorePlugin.ElseIfCondition` make.

    .. versionadded:: 5.0.0
    """

    equals = 0
    not_equals = 1
    contains = 2
    does_not_contain = 3
    greater_than = 4
    less_than = 5
    greater_than_or_equal = 6
    less_than_or_equal = 7
    regex_match = 8


class InstanceState(Enum):
    """Represents the state of an Instance and or Application inside an Instance."""

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
    awaiting_user_input = 80  # used during installation, means that some user input is required to complete setup (authentication etc).
    failed = 100
    suspended = 200
    maintenance = 250
    indeterminate = 999  # The state is unknown, or doesn't apply (for modules that don't start an external process)


class LoggingLevelState(Enum):
    """Related to Node: Core.Monitoring.LogLevel"""

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


class MailPriority(Enum):
    """The priority of an email sent by `EmailSenderPlugin.SendMail`.

    .. versionadded:: 5.0.0
    """

    normal = 0
    low = 1
    high = 2


class Module(StrEnum):
    ADS = "ADS"
    Minecraft = "Minecraft"
    Generic = "Generic"
    GenericModule = "GenericModule"
    SourceDedicatedServer = "SRCDS"


class PortAssignmentState(Enum):
    """Related to Node: ADSModule.Network.PortAssignment"""

    include_allowed_ports_only = 0
    allow_all_except_excluded = 1


class PostCreateState(Enum):
    """The action an Instance takes after it is created, AMP's `PostCreateAppActions`.

    Used by every `PostCreate` parameter (eg. `ADSModule/CreateInstance`, `ADSModule/DeployTemplate`) and the
    `ADSModule.Defaults.DefaultPostCreate` setting.

    """

    do_nothing = 0
    update_once = 1
    update_always = 2
    update_and_start_once = 3
    update_and_start_always = 4
    start_always = 5


class Protocols(Enum):
    """Related to :class:`PortInfo` from function :meth:`ADSModule.get_instance_network_info`.

    ```
    0 = TCP
    1 = UDP
    2 = TCP & UDP
    ```

    """

    TCP = 0
    UDP = 1
    TCP_and_UDP = 2


class ReleaseStreamState(Enum):
    """Related to Node: ADSModule.Defaults.DefaultReleaseStream"""

    lts = 5
    mainline = 10
    preview = 15
    development = 20


class TwoFactoryModeState(Enum):
    """Related to Node: Core.Security.TwoFactorMode"""

    optional = 0
    required = 1
