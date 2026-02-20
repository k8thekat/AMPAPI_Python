# AMP API Python

---

CubeCoders AMP API wrapper in Python.

<div align="left">
    <a href="https://discord.gg/BtNyU8DFtt"><img src='https://img.shields.io/discord/705500489248145459?color=blue&label=Discord&logo=Discord%20Server&logoColor=green' alt='Discord Server'></a>
</div>

<!-- ![Number of GitHub stars](https://img.shields.io/github/stars/d60/twikit) -->

![Version](https://img.shields.io/pypi/v/cubecoders-amp-api-wrapper?label=PyPI)

### Key Features

---

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
  - Optional parameter per function or global to disable formatting of data.
- Parent classes `ADSInstance` and `AMPInstance` to group endpoints together and make handling of multiple Instances easier.
  - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.

### Docs

- https://ampapi-python.readthedocs.io/en/latest/

### Installing

---

_Python 3.10 or higher is required_

To install run the below command to install the required pip packages from [Requirements](./requirements.txt)

### PyPi

---

-> Visit the package on [Pypi](https://pypi.org/project/cc-ampapi/)

```bash
# Linux/macOS/Windows
pip install cc-ampapi

```

### Basic Usage

---

In your IDE Python file. -> `import ampapi`.

1. First you need to fill out the APIParams class with the required fields (url, user and password).
2. Pass the APIParams class into the Bridge class parameter api_params.
   - You only need to make ONE bridge class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent class `ADSInstance()` or the smaller class `AMPInstance()` or any of the API classes as a stand alone.
   - See [Quick Example](https://github.com/k8thekat/AMPAPI_Python/blob/main/docs/samples/sample.py) for a visual example.

### Quick Example -

```py
from ampapi import *
from ampapi.dataclass import AnalyticsFilter, AnalyticsSummary, APIParams, Players
from ampapi.enums import *
from ampapi.instance import AMPControllerInstance, AMPInstance, AMPMinecraftInstance

# You can pull these values from an `.ini` or a `.env` file,
# then populate the NamedTuple APIparams from `types -> APIParams`
_params = APIParams(url="http://192.168.13.130:8080",
                    user="amp_username",
                    password="amp_password")



async def Sample_API() -> None:
    """
    Example API Function to call Endpoints.
    """
    _bridge = Bridge(api_params=_params)
    ADS: AMPControllerInstance = AMPControllerInstance()
    # By default all API calls will be formatted into Dataclasses if possible.
    # You can toggle format_data off with ANY of the API classes that inherit Base().
    ADS.format_data = False

    # This would populate the ADS class property .instances and .available_instances
    await ADS.get_instances(format_data=True)
    # We convert the ADS.instances attribute to a list for easier iteration.
    # The data is a set to prevent duplicates.
    ADSinstances = list(ADS.instances)
    arkinstance: Union[AMPInstance, None] = None
    mcinstance: Union[AMPInstance, AMPMinecraftInstance, None] = None
    # We can break out all our instances into their own attributes.
    for instance in ADSinstances:
        # Pre populated from the dataclass and has the API endpoints too!
        if isinstance(instance, (AMPADSInstance, AMPInstance, AMPMinecraftInstance)):
            if instance.friendly_name == "ArkInstance":
                arkinstance = instance
            elif instance.friendly_name == "Minecraft_PVP":
                mcinstance = instance

    if arkinstance is None or mcinstance is None or not isinstance(mcinstance, AMPMinecraftInstance):
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
    # Can be checked via `AMPInstance.Running`.
    # To keep this updated simply check.
    if mcinstance.running is True:
        print(f"{mcinstance.friendly_name} is Running Nyao~")

    elif mcinstance.running is False:
        print(f"{mcinstance.friendly_name} is not currently Running.")
        await mcinstance.start_instance()

    # You can also restart and stop the Instance too.
    await mcinstance.restart_instance()
    await mcinstance.stop_instance()

    # The State of the Application. eg. Running, Offline, Restarting, etc. See `types.py -> State_enum
    # This is NOT updated constantly. See about using `get_status()` to keep it current.
    if mcinstance.app_state == AMPInstanceState.stopped:
        await mcinstance.start_application()

    # You can also stop and update the application via
    await mcinstance.stop_application()
    await mcinstance.update_application()

    # To get more current Instance State check out.
    mcinstance.status.state
    mcinstance.app_state
    # To keep the `AMPInstance.State` property current; simply call the function below.
    await mcinstance.get_status()
    # You can also check Metrics of an Instance easily.
    mcinstance.status.metrics

    # Want to kick a random person? Here ya go~
    players: Players = await mcinstance.get_user_list()
    await mcinstance.mc_kick_user_by_id(user_id=players.sorted[0].uuid)



async def Sample_Analytics_API():
    """
    Example Method to use Instance Analytics.
    """
    ADS: AMPControllerInstance = AMPControllerInstance()
    await ADS.get_instances()
    # The index value to get to an MC Instance will be different for you; this is just an example.
    # You can check an Instances Type via the `.Module` attribute of any ADS/Instance class.
    mcinstance: AMPInstance | AMPMinecraftInstance = ADS.AvailableInstances[2]
    # Example analytics call without a filter.
    Analytics: Analytics_Summary = await mcinstance.get_analytics_summary()
    # Then with that class you can access lots of Information, such as Top Players, Stats and SessionTime.
    Analytics.topPlayers # This is a list of this Instances Top Players.
    Analytics.stats # This is a list of different fields such as Unique Users, New Users, etc..
    # _____________________________________________
    # Now you can also filter the results to look at a specific User or Country. Simply define the `Analytics_Filter` class and pass it into the method call.
    country_filter: Analytics_Filter = Analytics_Filter(Country="US") # The Country parameter supports `ISO 3166-1 Alpha-2 format` only.
    # These results will be filtered to only users within the US.
    filtered_analytics: Analytics_Summary = await mcinstance.get_analytics_summary(filters=country_filter)

    user_filter: Analytics_Filter = Analytics_Filter(Username="k8_thekat") # The IGN/Username of the user connected to the Server.
    # These results will be filtered to only users with that match the parameter Username. (eg. k8_thekat).
    filtered_analytics2: Analytics_Summary = await mcinstance.get_analytics_summary(filters=user_filter)


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

    $ This commit message will be omitted because of `$`
    - Everything below it will be ignored too as long as it has a `-`
```

#### AMP Version Bump

If the AMP version has changed, please generate new API spec sheets and upload them with any function changes.

- Run `await APIUtil.amp_api_update(instance=instance_here)`
