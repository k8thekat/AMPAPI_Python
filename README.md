# AMP API Python
___
CubeCoders AMP API wrapper in Python. 


<div align="left">
    <a href="https://discord.gg/BtNyU8DFtt"><img src='https://img.shields.io/discord/705500489248145459?color=blue&label=Discord&logo=Discord%20Server&logoColor=green' alt='Discord Server'></a>
</div>

<!-- ![Number of GitHub stars](https://img.shields.io/github/stars/d60/twikit) -->
![Version](https://img.shields.io/pypi/v/cubecoders-amp-api-wrapper?label=PyPI)


### Key Features
___

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
    - Optional parameter per function or global to disable formatting of data.
- Parent classes `ADSInstance` and `AMPInstance` to group endpoints together and make handling of multiple Instances easier.
    - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.

### Installing
___

*Python 3.10 or higher is required*

To install run the below command to install the required pip packages from [Requirements](./requirements.txt)

### PyPi 
___
-> Visit the package on [Pypi](https://pypi.org/project/cc-ampapi/)

```bash
# Linux/macOS/Windows
pip install cc-ampapi

```

### Basic Usage
___
1. First you need to fill out the APIParams class with the required fields (url, user and password).
2. Pass the APIParams class into the Bridge class parameter api_params.
    - You only need to make ONE bridge class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent class `ADSInstance()` or the smaller class `AMPInstance()` or any of the API classes as a stand alone.
    - See [Quick Example](./README.md#quick-example--) for a visual example.

### Quick Example -

```py
# You can pull these values from an `.ini` or a `.env` file,
# then populate the NamedTuple APIparams from `types -> APIParams`
_params = APIParams(url="http://192.168.13.130:8080",
                    user="amp_username",
                    password="amp_password")

_bridge = Bridge(api_params=_params)

async def Sample_API():
    """
    Example Method to call Instance Endpoints and create the ADS Instance class.
    """
    
    ADS: ADSInstance = ADSInstance()
    # This would populate the ADS class property .AvailableInstances
    await ADS.get_instances()
    # We can break out all our instances into their own attributes.
    # Your instances wont line up like these examples; but you can check the InstanceName and Module to figure out the order of your Instances.
    arkinstance: AMPInstance | AMPMinecraftInstance = ADS.AvailableInstances[1]
    mcinstance: AMPInstance | AMPMinecraftInstance = ADS.AvailableInstances[2]

    # Pre populated from the dataclass and has the API methods too!
    # You can take a backup really easily.
    await arkinstance.take_backup(title="ARK1_backup", description="This is an ARK backup", sticky=True)

    # Then you can call instance type specific API methods.
    await mcinstance.mc_add_to_whitelist(user_or_uuid="k8_thekat")

    # You can also check attributes and other fields of the instance.
    mcinstance.InstanceName
    mcinstance.InstanceID

    # The State of the Instance. eg. Running, Offline, Restarting. See `types.py -> State_enum
    # This is NOT updated constantly. See about using `get_status()` to keep it current.
    if mcinstance.AppState == State_enum.Stopped:
        await mcinstance.start_instance()

    # You can also check Metrics of an Instance easily.
    mcinstance.Status.Metrics

    # Want to kick a random person? Here ya go~
    players: list[Players] = await mcinstance.get_user_list()
    await mcinstance.mc_kick_user_by_id(id=players[0].id)


async def Sample_Analytics_API():
    """
    Example Method to use Instance Analytics.
    """
    ADS: ADSInstance = ADSInstance()
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
# By default all API calls will be formatted into Dataclasses if possible.
# You can toggle format_data off with ANY of the API classes that inherit Base().
ADS.format_data = False

# You can turn data formatting back on globally through any Instance object.
arkinstance.format_data = True

# You can turn off or on data formatting per function also.
await arkinstance.get_updates(format_data=False)
await arkinstance.get_role_data(format_data=True)

```


### Contributing to the project

# Git Commit message format

```
    # file_name.py 
    - Change 1
    - Change 2
    -- Change 2 sub-change 1

    $ This commit message will be omitted because of `$`
    - Everything below it will be ignored too as long as it has a `-`
```

# AMP Version Bump
If the AMP version has changed, please generate new API spec sheets and upload them with any function changes.
- Run `await APIUtil.amp_api_update(instance=instance_here)`

