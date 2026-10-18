# AMP API Python

---

An asynchronous Python wrapper for the CubeCoders AMP (Application Management Panel) API, enabling developers to programmatically manage game server instances with a clean, Pythonic interface.

<div align="left">
    <a href="https://discord.gg/BtNyU8DFtt"><img src='https://img.shields.io/discord/705500489248145459?color=blue&label=Discord&logo=Discord%20Server&logoColor=green' alt='Discord Server'></a>
</div>

<!-- ![Number of GitHub stars](https://img.shields.io/github/stars/d60/twikit) -->

![Version](https://img.shields.io/pypi/v/cc-ampapi?label=PyPI)

### Table of Contents

---

- [Key Features](#key-features)
- [Docs](#docs)
- [Installing](#installing)
  - [PyPi](#pypi)
- [Upgrading from 4.x](#upgrading-from-4x)
- [Basic Usage](#basic-usage)
  - [Quick Example](#quick-example--)
- [Controlling data formatting](#controlling-data-formatting--)
- [Contributing to the Project](#contributing-to-the-project)
- [Issues]
- [Changelog]

### Key Features

---

- Pythonic API wrapper using `async` and `await` via `aiohttp`.
- Data is automatically deserialized into typed dataclasses for easier management and interaction.
  - Optional parameter per function or global to disable formatting of data.
- Inheritance-based instance model (`Controller`, `Instance`, `MinecraftInstance`, etc.) groups endpoints by instance type, preventing invalid calls at the class level.
- TOTP/2FA authentication support for secure programmatic login via `pyotp`.
- Fully typed and verified with Pyright in strict mode, compatible with Python 3.12+.

### Docs

- https://ampapi-python.readthedocs.io/en/latest/

### Installing

---

_Python 3.12 or higher is required_

To install run the below command via your preferred terminal or IDE.

### PyPi

---

-> Visit the package on [Pypi](https://pypi.org/project/cc-ampapi/)

```bash
# Linux/macOS/Windows
pip install cc-ampapi

```

### Upgrading from 4.x

---

**5.0.0 is a major version bump, because it breaks backwards compatibility with 4.x.**
Code written for `4.6.0` will need a few changes before it runs, so pin `cc-ampapi<5` if you aren't ready to upgrade yet~

- Requirements
  - Python 3.12 or higher (4.x supported 3.10).
  - AMP `2.6.2.8` or newer. The session is sent in the `Authorization` header now, and the old `SESSIONID` parameter is gone.
- Renamed classes
  - `AMPControllerInstance` -> `Controller`
  - `AMPInstance` -> `Instance`
  - `AMPMinecraftInstance` -> `MinecraftInstance`
  - `AMPADSInstance` -> `TargetADS`
  - `AMPInstanceState` -> `InstanceState`
- Moved modules (everything public is still available straight from `ampapi`)
  - `ampapi.controller` was removed; `Controller` lives in `ampapi.instance`.
  - `ampapi.enums_` -> `ampapi._enums`
  - `ampapi.types_` -> `ampapi._types`
- Errors
  - API errors are now raised (see `ampapi.errors`) instead of an `ActionResultError` being returned.

### Basic Usage

---

In your IDE Python file. -> `import ampapi`.

1. First you need to fill out the APIParams class with the required fields (url, user and password).
2. Pass the APIParams class into the Bridge class parameter api_params.
   - You only need to make ONE bridge class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent class `Controller()` or the smaller class `Instance()` or any of the API classes as a stand alone.
   - See [Quick Example](https://github.com/k8thekat/AMPAPI_Python/blob/main/docs/samples/sample.py) for a visual example.

### Quick Example -

```py
from typing import Union

from ampapi import (
    AnalyticsFilter,
    AnalyticsSummary,
    APIParams,
    Bridge,
    Controller,
    Instance,
    InstanceState,
    MinecraftInstance,
    Players,
)

# You can pull these values from an `.ini` or a `.env` file,
# then populate the dataclass APIParams from `modules -> APIParams`
_params = APIParams(url="http://192.168.13.130:8080",
                    user="amp_username",
                    password="amp_password")



async def Sample_API() -> None:
    """
    Example API Function to call Endpoints.
    """
    _bridge = Bridge(api_params=_params)
    ADS: Controller = Controller()
    # By default all API calls will be formatted into Dataclasses if possible.
    # You can toggle format_data off with ANY of the API classes that inherit Base().
    ADS.format_data = False

    # This would populate the ADS class property .instances
    await ADS.get_instances(format_data=True)
    # We convert the ADS.instances attribute to a list for easier iteration.
    # The data is a set to prevent duplicates.
    ADSinstances = list(ADS.instances)
    arkinstance: Union[Instance, None] = None
    mcinstance: Union[Instance, MinecraftInstance, None] = None
    # We can break out all our instances into their own attributes.
    for instance in ADSinstances:
        # Pre populated from the dataclass and has the API endpoints too!
        if isinstance(instance, Instance):
            if instance.friendly_name == "ArkInstance":
                arkinstance = instance
            elif instance.friendly_name == "Minecraft_PVP":
                mcinstance = instance

    if arkinstance is None or mcinstance is None or not isinstance(mcinstance, MinecraftInstance):
        return
    # This turns back on data formatting Globally.
    arkinstance.format_data = True

    # You can take a backup really easily.
    await arkinstance.take_backup(name="ARK1_backup", description="This is an ARK backup", sticky=True)

    # Then you can call instance type specific API endpoints.
    await mcinstance.mc_add_to_whitelist(user_or_uuid="k8_thekat")

    # You can also check attributes and other fields of the instance for easy logic.
    if mcinstance.instance_name == "Test_Server":
        # do code here
        ...

    # The State of the Instance.
    # Can be checked via `Instance.running`.
    # This is cached, call `ADS.get_instances()` again to refresh it.
    if mcinstance.running is True:
        print(f"{mcinstance.friendly_name} is Running Nyao~")

    elif mcinstance.running is False:
        print(f"{mcinstance.friendly_name} is not currently Running.")
        await mcinstance.start_instance()

    # You can also restart and stop the Instance too.
    await mcinstance.restart_instance()
    await mcinstance.stop_instance()

    # The State of the Application. eg. ready, stopped, restarting, etc. See `_enums.py -> InstanceState`
    # This is NOT updated constantly. See about using `get_status()` to get it current.
    if mcinstance.app_state == InstanceState.stopped:
        await mcinstance.start_application()

    # You can also stop and update the application via
    await mcinstance.stop_application()
    await mcinstance.update_application()

    # To get the current Instance State call the function below, it returns a `Status` dataclass.
    status = await mcinstance.get_status()
    status.state
    # You can also check Metrics of an Instance easily.
    status.metrics

    # Want to kick a random person? Here ya go~
    players: Players = await mcinstance.get_user_list()
    await mcinstance.mc_kick_user_by_id(user_id=players.sorted[0].uuid)



async def Sample_Analytics_API():
    """
    Example Method to use Instance Analytics.
    """
    ADS: Controller = Controller()
    await ADS.get_instances()
    # The instances are a set, so we pick the first Minecraft one out of it; this is just an example.
    # You can check an Instances Type via the `.module` attribute of any Instance class.
    mcinstance: Union[Instance, MinecraftInstance, None] = None
    for instance in ADS.instances:
        if isinstance(instance, MinecraftInstance):
            mcinstance = instance
            break
    if mcinstance is None:
        return
    # Example analytics call without a filter.
    Analytics: AnalyticsSummary = await mcinstance.get_analytics_summary()
    # Then with that class you can access lots of Information, such as Top Players, Stats and SessionTime.
    Analytics.top_players # This is a list of this Instances Top Players.
    Analytics.stats # This is a list of different fields such as Unique Users, New Users, etc..
    # _____________________________________________
    # Now you can also filter the results to look at a specific User or Country. Simply define the `AnalyticsFilter` class and pass it into the method call.
    country_filter: AnalyticsFilter = AnalyticsFilter(country="US") # The country parameter supports `ISO 3166-1 Alpha-2 format` only.
    # These results will be filtered to only users within the US.
    filtered_analytics: AnalyticsSummary = await mcinstance.get_analytics_summary(filters=country_filter)

    user_filter: AnalyticsFilter = AnalyticsFilter(username="k8_thekat") # The IGN/Username of the user connected to the Server.
    # These results will be filtered to only users with that match the parameter username. (eg. k8_thekat).
    filtered_analytics2: AnalyticsSummary = await mcinstance.get_analytics_summary(filters=user_filter)


```

### Controlling data formatting -

- All JSON data returned from the API endpoints is formatted into a Dataclass/Enum/etc if possible.
- Data formatting can be controlled globally or locally by changing the `format_data` parameter of the method to `False`.
  - When turning off the data formatting, typically you will get a `dictionary` back.

### Example -

```py
# You must have your Bridge object made and the Instance class created to access `format_data`.
# By default all API calls will be formatted into Dataclasses if possible.
# You can toggle format_data off with ANY of the API classes that inherit Base().
ADS.format_data = False

# You can turn data formatting back on globally through any Instance object.
arkinstance.format_data = True

# You can turn off or on data formatting per function also.
await arkinstance.get_updates(format_data=False)
await arkinstance.get_role_data(format_data=True)

```

# Contributing to the Project

#### Git Commit message format

```
    # file_name.py
    - Change 1
    - Change 2
    -- Change 2 sub-change 1

    $ Only this line is omitted from the changelog, because it starts with `$`
    $ A line after it is kept unless it also starts with `$`, so prefix every line to hide
```

#### AMP Version Bump

If the AMP version has changed, please generate new API spec sheets and upload them with any function changes.

- Run `await amp_api_update(instance=controller_here, sanitize_json=True)` from `ampapi.util`, where `controller_here` is your `Controller`.

[Issues]: https://github.com/k8thekat/AMPAPI_Python/issues
[Changelog]: https://github.com/k8thekat/AMPAPI_Python/blob/main/CHANGELOG.md
